import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(
    title="Google MCP Server",
    description="An MCP-style server to integrate with Google Docs and Gmail.",
    version="1.0.0"
)

class AppendDocRequest(BaseModel):
    doc_id: str
    content: str

class EmailDraftRequest(BaseModel):
    to: str
    subject: str
    body: str

def prompt_approval(action_name: str, payload: dict) -> bool:
    """
    Prints the action name and payload to the terminal and asks for user approval.
    """
    print("\n" + "="*50)
    print(f"ACTION REQUIRED: {action_name}")
    print("Payload:")
    for k, v in payload.items():
        print(f"  {k}: {v}")
    print("="*50)
    
    # Auto-approve if on Railway
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        print("Running on Railway. Auto-approving action.")
        return True
    
    # Prompt user for approval
    # Note: When running uvicorn in an interactive terminal, input() works fine.
    try:
        response = input("Approve? (y/n): ").strip().lower()
        return response == 'y'
    except EOFError:
        print("\nEOF encountered while waiting for input. Rejecting.")
        return False
    except Exception as e:
        print(f"\nError reading input: {e}. Rejecting.")
        return False

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Google MCP Server is running.",
        "endpoints": [
            "/append_to_doc",
            "/create_email_draft"
        ]
    }

@app.post("/append_to_doc")
def api_append_to_doc(request: AppendDocRequest):
    payload = request.model_dump()
    if not prompt_approval("Append to Google Doc", payload):
        raise HTTPException(status_code=403, detail="Action rejected by user.")
    
    try:
        result = append_to_doc(request.doc_id, request.content)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_email_draft")
def api_create_email_draft(request: EmailDraftRequest):
    payload = request.model_dump()
    if not prompt_approval("Create Gmail Draft", payload):
        raise HTTPException(status_code=403, detail="Action rejected by user.")
    
    try:
        result = create_email_draft(request.to, request.subject, request.body)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("RAILWAY_ENVIRONMENT") else "127.0.0.1"
    uvicorn.run("server:app", host=host, port=port, reload=not os.environ.get("RAILWAY_ENVIRONMENT"))
