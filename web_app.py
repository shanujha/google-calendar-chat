"""
Google Calendar Chat Agent - Web UI
A web-based interface for the AI chat agent
"""

import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import secrets

# Import the chat agent classes
from calendar_chat import CalendarService, GeminiAgent, CalendarChatAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))

# Store chat agents per session (in production, use Redis or similar)
chat_agents = {}


def get_or_create_agent(session_id: str, gemini_api_key: str):
    """Get existing agent or create new one for session"""
    if session_id not in chat_agents:
        try:
            chat_agents[session_id] = CalendarChatAgent(gemini_api_key)
        except Exception as e:
            return None, str(e)
    return chat_agents[session_id], None


@app.route('/')
def index():
    """Main page"""
    # Check if user has set up their API key
    has_api_key = 'gemini_api_key' in session and session['gemini_api_key']
    return render_template('index.html', has_api_key=has_api_key)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Setup page for API key configuration"""
    if request.method == 'POST':
        gemini_api_key = request.form.get('gemini_api_key', '').strip()
        
        if not gemini_api_key:
            return render_template('setup.html', error='Please provide a valid Gemini API key')
        
        # Store in session
        session['gemini_api_key'] = gemini_api_key
        session['session_id'] = secrets.token_hex(16)
        
        # Try to initialize the agent
        agent, error = get_or_create_agent(session['session_id'], gemini_api_key)
        if error:
            return render_template('setup.html', error=f'Failed to initialize: {error}')
        
        return redirect(url_for('chat'))
    
    return render_template('setup.html')


@app.route('/chat')
def chat():
    """Chat interface"""
    if 'gemini_api_key' not in session:
        return redirect(url_for('setup'))
    
    return render_template('chat.html')


@app.route('/api/message', methods=['POST'])
def send_message():
    """Handle chat messages"""
    if 'gemini_api_key' not in session or 'session_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Get or create agent
    agent, error = get_or_create_agent(session['session_id'], session['gemini_api_key'])
    if error:
        return jsonify({'error': error}), 500
    
    # Process the message
    try:
        response = agent.process_query(user_message)
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500


@app.route('/api/events')
def get_events():
    """Get calendar events"""
    if 'gemini_api_key' not in session or 'session_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    agent, error = get_or_create_agent(session['session_id'], session['gemini_api_key'])
    if error:
        return jsonify({'error': error}), 500
    
    try:
        events = agent.calendar.list_events(max_results=10)
        formatted_events = []
        for event in events:
            formatted_events.append({
                'id': event.get('id'),
                'summary': event.get('summary', 'No title'),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'description': event.get('description', '')
            })
        return jsonify({'events': formatted_events})
    except Exception as e:
        return jsonify({'error': f'Error fetching events: {str(e)}'}), 500


@app.route('/logout')
def logout():
    """Clear session and logout"""
    session_id = session.get('session_id')
    if session_id and session_id in chat_agents:
        del chat_agents[session_id]
    
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Google Calendar Chat Agent - Web UI")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
