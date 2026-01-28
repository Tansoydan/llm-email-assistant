import base64
from email.message import EmailMessage
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def get_gmail_service(credentials_path: str = "credentials.json", token_path: str = "token.json"):
    creds = None
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    except Exception:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _get_header(headers: List[Dict[str, str]], name: str) -> Optional[str]:
    name_lower = name.lower()
    for h in headers:
        if h.get("name", "").lower() == name_lower:
            return h.get("value")
    return None


def _decode_base64url(data: str) -> str:
    if not data:
        return ""
    missing_padding = 4 - (len(data) % 4)
    if missing_padding and missing_padding != 4:
        data += "=" * missing_padding
    return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")


def _extract_text_from_payload(payload: dict) -> str:
    # Prefer text/plain parts when possible
    if "parts" in payload:
        texts = []
        for part in payload["parts"]:
            mime = part.get("mimeType", "")
            body = part.get("body", {})
            data = body.get("data")

            if mime == "text/plain" and data:
                texts.append(_decode_base64url(data))
            elif mime.startswith("multipart/"):
                texts.append(_extract_text_from_payload(part))
            # Ignore HTML for v1 (you can add html->text later)
        return "\n".join([t for t in texts if t.strip()])

    body = payload.get("body", {})
    data = body.get("data")
    if data:
        return _decode_base64url(data)
    return ""


def list_message_ids(service, query: str = "newer_than:7d", max_results: int = 10) -> List[str]:
    res = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    msgs = res.get("messages", [])
    return [m["id"] for m in msgs]


def fetch_message(service, message_id: str) -> Dict[str, str]:
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    payload = msg.get("payload", {})
    headers = payload.get("headers", [])
    subject = _get_header(headers, "Subject") or ""
    sender = _get_header(headers, "From") or ""
    to = _get_header(headers, "To") or ""
    date = _get_header(headers, "Date") or ""
    text = _extract_text_from_payload(payload)

    return {
        "id": message_id,
        "subject": subject,
        "from": sender,
        "to": to,
        "date": date,
        "text": text.strip(),
    }


def create_draft_reply(service, to_email: str, subject: str, body_text: str, thread_id: Optional[str] = None) -> str:
    message = EmailMessage()
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body_text)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    draft_body = {"message": {"raw": raw}}
    if thread_id:
        draft_body["message"]["threadId"] = thread_id

    draft = service.users().drafts().create(userId="me", body=draft_body).execute()
    return draft.get("id", "")
