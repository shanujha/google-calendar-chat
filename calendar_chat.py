"""
Google Calendar Chat Agent
An AI-based chat interface for Google Calendar using Gemini API
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarService:
    """Handles Google Calendar API operations"""
    
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Calendar API using OAuth2"""
        creds = None
        
        # Token file stores user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("\n⚠️  Error: credentials.json not found!")
                    print("Please follow these steps:")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a project or select an existing one")
                    print("3. Enable Google Calendar API")
                    print("4. Create OAuth 2.0 credentials (Desktop app)")
                    print("5. Download the credentials as 'credentials.json'")
                    print("6. Place it in the project root directory\n")
                    sys.exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
        print("✅ Successfully authenticated with Google Calendar\n")
    
    def list_events(self, max_results: int = 10, time_min: Optional[datetime] = None, 
                   time_max: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """List calendar events"""
        try:
            if time_min is None:
                time_min = datetime.utcnow()
            
            time_min_str = time_min.isoformat() + 'Z'
            time_max_str = time_max.isoformat() + 'Z' if time_max else None
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min_str,
                timeMax=time_max_str,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def create_event(self, summary: str, start_time: datetime, end_time: datetime,
                    description: str = "", location: str = "") -> Dict[str, Any]:
        """Create a new calendar event"""
        try:
            event = {
                'summary': summary,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            return event
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {}
    
    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event"""
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def update_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """Update an existing calendar event"""
        try:
            event = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            # Update fields
            for key, value in kwargs.items():
                if key in event:
                    event[key] = value
            
            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return updated_event
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {}


class GeminiAgent:
    """AI agent using Gemini API for natural language understanding"""
    
    def __init__(self, api_key: str):
        if not api_key:
            print("\n⚠️  Error: GEMINI_API_KEY not found!")
            print("Please set your Gemini API key:")
            print("1. Get your API key from https://makersuite.google.com/app/apikey")
            print("2. Set it as environment variable: export GEMINI_API_KEY='your-key'")
            print("   Or create a .env file with: GEMINI_API_KEY=your-key\n")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        print("✅ Successfully initialized Gemini AI\n")
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate a response using Gemini"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def parse_calendar_command(self, user_input: str, calendar_context: str) -> Dict[str, Any]:
        """Parse user input to understand calendar intent"""
        system_context = """You are a helpful calendar assistant. Analyze the user's request and determine:
1. The action they want to perform (list, create, delete, update)
2. Extract relevant details (date, time, event name, duration, etc.)
3. Return a JSON response with this structure:
{
    "action": "list|create|delete|update",
    "summary": "event title",
    "start_time": "ISO datetime string",
    "end_time": "ISO datetime string",
    "description": "event description",
    "confidence": "high|medium|low",
    "clarification_needed": "question if details are unclear"
}

Current calendar context:
""" + calendar_context
        
        prompt = f"{system_context}\n\nUser request: {user_input}\n\nProvide your analysis as JSON only, no additional text."
        
        response = self.generate_response(prompt)
        
        # Try to extract JSON from response
        try:
            # Find JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {"action": "unknown", "confidence": "low", 
                       "clarification_needed": "Could not understand the request"}
        except json.JSONDecodeError:
            return {"action": "unknown", "confidence": "low",
                   "clarification_needed": "Could not parse the request"}


class CalendarChatAgent:
    """Main chat agent that coordinates calendar and AI operations"""
    
    def __init__(self, gemini_api_key: str):
        self.calendar = CalendarService()
        self.ai = GeminiAgent(gemini_api_key)
        self.conversation_history = []
    
    def format_events(self, events: List[Dict[str, Any]]) -> str:
        """Format events for display and AI context"""
        if not events:
            return "No upcoming events found."
        
        formatted = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No title')
            event_id = event.get('id', '')
            formatted.append(f"- {start}: {summary} (ID: {event_id[:8]}...)")
        
        return "\n".join(formatted)
    
    def get_calendar_context(self) -> str:
        """Get current calendar state for AI context"""
        events = self.calendar.list_events(max_results=10)
        return f"Upcoming events:\n{self.format_events(events)}"
    
    def process_query(self, user_input: str) -> str:
        """Process user query and execute appropriate action"""
        
        # Get current calendar context
        context = self.get_calendar_context()
        
        # Simple command handling for common requests
        user_input_lower = user_input.lower()
        
        # List events
        if any(keyword in user_input_lower for keyword in ['list', 'show', 'what', 'upcoming', 'events']):
            events = self.calendar.list_events(max_results=10)
            if events:
                response = "Here are your upcoming events:\n\n" + self.format_events(events)
            else:
                response = "You have no upcoming events."
            return response
        
        # For complex queries, use AI
        parsed = self.ai.parse_calendar_command(user_input, context)
        
        if parsed.get('action') == 'create':
            # Handle event creation
            try:
                # Extract datetime - simplified version
                # In production, you'd want more robust parsing
                summary = parsed.get('summary', 'New Event')
                # Default to 1 hour from now
                start_time = datetime.utcnow() + timedelta(hours=1)
                end_time = start_time + timedelta(hours=1)
                
                event = self.calendar.create_event(
                    summary=summary,
                    start_time=start_time,
                    end_time=end_time,
                    description=parsed.get('description', '')
                )
                
                if event:
                    return f"✅ Created event: {summary}\nStart: {start_time}\nEnd: {end_time}"
                else:
                    return "❌ Failed to create event"
            except Exception as e:
                return f"Error creating event: {str(e)}"
        
        # If we need clarification or can't determine action
        if parsed.get('clarification_needed'):
            return f"🤔 {parsed['clarification_needed']}"
        
        # Use AI for general conversation
        ai_response = self.ai.generate_response(
            user_input,
            context=f"You are a calendar assistant. Here's the current calendar:\n{context}"
        )
        
        return ai_response
    
    def start_chat(self):
        """Start interactive chat session"""
        print("="*60)
        print("🗓️  Google Calendar Chat Agent")
        print("="*60)
        print("\nWelcome! I can help you manage your Google Calendar.")
        print("\nTry commands like:")
        print("  - 'Show my upcoming events'")
        print("  - 'List my events'")
        print("  - 'What's on my calendar?'")
        print("  - 'Create an event for tomorrow'")
        print("\nType 'quit' or 'exit' to end the session.\n")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Have a great day!\n")
                    break
                
                # Process the query
                response = self.process_query(user_input)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  Google Calendar Chat Agent - Initialization")
    print("="*60 + "\n")
    
    # Get Gemini API key
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_api_key:
        print("⚠️  GEMINI_API_KEY not found in environment variables")
        gemini_api_key = input("Please enter your Gemini API key: ").strip()
        
        if not gemini_api_key:
            print("❌ API key is required. Exiting.")
            sys.exit(1)
    
    # Initialize and start chat agent
    try:
        agent = CalendarChatAgent(gemini_api_key)
        agent.start_chat()
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
