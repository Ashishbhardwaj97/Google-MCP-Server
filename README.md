# Google-MCP-Server

A lightweight, Python-based Model Context Protocol (MCP) server that securely integrates with Google Workspace using FastAPI and OAuth 2.0.

It uses Google OAuth 2.0 to access the user's Docs and Gmail accounts to:
- Append text to a Google Doc.
- Create a Gmail draft.

## Prerequisites

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Docs API** and **Gmail API**.
3. Configure the OAuth consent screen and create an OAuth 2.0 Client ID for a "Desktop app".
4. Download the JSON credentials file and save it as `credentials.json` in this directory.

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Server

Start the FastAPI server using Uvicorn:

```bash
python server.py
# or
uvicorn server:app
```

The server will be available at `http://localhost:8000`. 
API documentation is available at `http://localhost:8000/docs`.

### Approval Flow

This server includes an interactive approval step. When an endpoint is called, the server will print the action details to the terminal and wait for you to type `y` to approve or anything else to reject. **Make sure you run the server in an interactive terminal.**
