# Setting Up Google Calendar API Credentials

This guide will help you create the `credentials.json` file needed for the Google Calendar Chat Agent.

## Step-by-Step Instructions

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Calendar Chat Agent")
5. Click "Create"

### 2. Enable Google Calendar API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### 3. Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" (unless you're using Google Workspace)
3. Click "Create"
4. Fill in the required fields:
   - App name: "Calendar Chat Agent" (or your preferred name)
   - User support email: Your email
   - Developer contact information: Your email
5. Click "Save and Continue"
6. On the Scopes page, click "Save and Continue" (no additional scopes needed)
7. On the Test users page, add your email address
8. Click "Save and Continue"

### 4. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Desktop app" as the application type
4. Enter a name (e.g., "Calendar Chat Desktop Client")
5. Click "Create"
6. A dialog will appear with your credentials. Click "Download JSON"

### 5. Save the Credentials File

1. Rename the downloaded file to `credentials.json`
2. Move it to the root directory of this project (same folder as `calendar_chat.py`)

## Important Notes

- **Security**: Never commit `credentials.json` to version control
- The `.gitignore` file is already configured to exclude it
- Keep this file secure and don't share it publicly
- If you accidentally expose it, delete it from Google Cloud Console and create a new one

## Expected credentials.json Structure

Your `credentials.json` should look something like this (with your actual values):

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}
```

## First-Time Authentication

When you run the application for the first time:

1. A browser window will open automatically
2. Sign in with your Google account
3. Grant the requested permissions
4. The application will save a `token.json` file for future use
5. You won't need to authenticate again unless you delete `token.json`

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you've added your email as a test user in the OAuth consent screen
- Verify that the Google Calendar API is enabled

### "The redirect URI in the request did not match a registered redirect URI"
- Make sure you selected "Desktop app" when creating the OAuth client

### "credentials.json not found"
- Verify the file is in the project root directory
- Check that it's named exactly `credentials.json` (case-sensitive)

## Need Help?

If you encounter any issues, please check the [main README](README.md) or open an issue on the GitHub repository.
