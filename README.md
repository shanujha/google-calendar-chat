# Google Calendar Chat Agent 🗓️🤖

An AI-based chat agent that interfaces with Google Calendar using Google's Gemini API. Manage your calendar through natural language conversations with both **Web UI** and **CLI** interfaces!

## Features

- 🌐 **Web Interface**: Modern, responsive web UI for easy interaction
- 🤖 **Natural Language Interface**: Chat with your calendar using everyday language
- 🔐 **Secure Authentication**: OAuth2 authentication for Google Calendar
- 🔑 **Personal Gemini API**: Use your own Gemini API key for AI-powered interactions
- 📅 **Calendar Management**: List, create, update, and delete events
- 💬 **Conversational AI**: Powered by Google's Gemini AI model
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Python 3.7 or higher
- A Google Account with Calendar access
- A Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shanujha/google-calendar-chat.git
cd google-calendar-chat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or create a virtual environment first (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Google Calendar API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Calendar API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials
5. Save the downloaded file as `credentials.json` in the project root directory

### 4. Set Up Gemini API Key

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

You can provide the API key in two ways:

**Option 1: Environment Variable**
```bash
export GEMINI_API_KEY='your-api-key-here'
```

**Option 2: .env File**
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-api-key-here
```

## Usage

You can run the application in two ways:

### Option 1: Web Interface (Recommended)

Start the web server:

```bash
python web_app.py
```

Then open your browser and navigate to `http://localhost:5000`

**Features of the Web UI:**
- 🎨 Beautiful, modern interface
- 💬 Real-time chat with your calendar
- 📋 Live event list in the sidebar
- 📱 Mobile-friendly responsive design
- 🔒 Secure session-based API key storage

On first visit, you'll be guided through:
1. Entering your Gemini API key
2. Authenticating with Google Calendar (browser OAuth flow)
3. Starting your chat session

### Option 2: Command Line Interface

Run the CLI chat agent:

```bash
python calendar_chat.py
```

On first run, you'll be prompted to authenticate with Google Calendar through your browser.

### Example Commands

Once the chat agent is running (web or CLI), try these commands:

- **List Events**: 
  - "Show my upcoming events"
  - "What's on my calendar?"
  - "List my events"

- **General Queries**:
  - "What do I have tomorrow?"
  - "Am I free this afternoon?"
  - "Tell me about my schedule"

- **Create Events** (Basic):
  - "Create an event"
  - "Schedule a meeting"

### CLI Chat Interface

```
============================================================
🗓️  Google Calendar Chat Agent
============================================================

Welcome! I can help you manage your Google Calendar.

Try commands like:
  - 'Show my upcoming events'
  - 'List my events'
  - 'What's on my calendar?'
  - 'Create an event for tomorrow'

Type 'quit' or 'exit' to end the session.

============================================================

You: show my events
```

## Architecture

The application consists of multiple components:

### Backend Components

1. **CalendarService**: Handles Google Calendar API operations (list, create, update, delete events)
2. **GeminiAgent**: Manages AI interactions using Google's Gemini API for natural language understanding
3. **CalendarChatAgent**: Coordinates between the calendar service and AI agent to process user queries

### Web UI Components

4. **Flask Web Server** (`web_app.py`): Provides RESTful API and serves the web interface
5. **HTML Templates**: Modern, responsive UI with chat interface and event sidebar
6. **JavaScript**: Real-time chat functionality and event updates

## Files

### Core Application
- `calendar_chat.py`: CLI chat agent
- `web_app.py`: Web server and API endpoints
- `requirements.txt`: Python dependencies

### Web UI
- `templates/`: HTML templates for web interface
  - `base.html`: Base template with navigation
  - `index.html`: Landing page
  - `setup.html`: API key setup page
  - `chat.html`: Chat interface
- `static/css/style.css`: Responsive CSS styling
- `static/js/chat.js`: Client-side chat functionality

### Configuration
- `credentials.json`: Google OAuth credentials (you need to create this)
- `token.json`: Stored OAuth tokens (automatically created after first login)
- `.env`: Environment variables (optional, for storing API keys)

## Security Notes

- Never commit `credentials.json`, `token.json`, or `.env` files to version control
- Keep your Gemini API key secure and don't share it publicly
- The `.gitignore` file is configured to exclude sensitive files

## Troubleshooting

### "credentials.json not found"
- Make sure you've downloaded the OAuth credentials from Google Cloud Console
- Save it as `credentials.json` in the project root directory

### "GEMINI_API_KEY not found"
- Set the environment variable or create a `.env` file with your API key
- Get your API key from https://makersuite.google.com/app/apikey

### Authentication Issues
- Delete `token.json` and try authenticating again
- Make sure you've enabled Google Calendar API in your Google Cloud project

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/shanujha/google-calendar-chat/issues).
