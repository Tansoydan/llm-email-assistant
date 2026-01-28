import os
from dotenv import load_dotenv

from dotenv import load_dotenv

from src.gmail_client import (
    get_gmail_service,
    list_message_ids,
    fetch_message,
    create_draft_reply,
)
from src.classifier import classify_email


load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "phi3")
QUERY = os.getenv("GMAIL_QUERY", "newer_than:7d")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", "5"))

def main():
    service = get_gmail_service()

    ids = list_message_ids(service, query=QUERY, max_results=MAX_RESULTS)
    if not ids:
        print("No emails found for query:", QUERY)
        return

    for mid in ids:
        email = fetch_message(service, mid)

        if not email["text"]:
            print(f"\n[{mid}] Skipping (no plain text body). Subject: {email['subject']}")
            continue

        result = classify_email(MODEL, email)

        print("\n==============================")
        print("From:", email["from"])
        print("Subject:", email["subject"])
        print("Label:", result.get("label"))
        print("Confidence:", result.get("confidence"))
        print("Reason:", result.get("reason"))

        # Example: draft a reply only for action_required/urgent
        if result.get("label") in ("urgent", "action_required"):
            draft_body = f"""Hi,

Thanks for your email — I’ve seen this and I’m on it.
Quick clarifying question: what’s your ideal deadline?

Best,
Tan
"""
            # NOTE: "From" header can include name + email; you'd parse properly in v2
            to_email = email["from"]
            draft_id = create_draft_reply(
                service,
                to_email=to_email,
                subject=f"Re: {email['subject']}".strip(),
                body_text=draft_body,
            )
            print("Draft created:", draft_id)

if __name__ == "__main__":
    main()
