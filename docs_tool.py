from googleapiclient.discovery import build
from auth import get_credentials

def append_to_doc(doc_id: str, content: str) -> dict:
    """
    Appends text to the end of a Google Doc.
    
    Args:
        doc_id: The ID of the Google Doc.
        content: The text to append.
        
    Returns:
        The response from the Google Docs API.
    """
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    # Note: To append to the end of the document, we can use an InsertTextRequest
    # with an endOfSegmentLocation.
    requests = [
        {
            "insertText": {
                "endOfSegmentLocation": {
                    "segmentId": ""  # empty string means the body of the document
                },
                "text": content
            }
        }
    ]

    result = service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()
    
    return result
