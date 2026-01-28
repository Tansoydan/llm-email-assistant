LLM Email Assistant (Local)

A local LLM-powered email assistant that connects to Gmail, classifies incoming emails by intent using Ollama (phi3), and optionally creates draft replies for high-priority messages.

The system runs entirely locally (no cloud LLM APIs) and is designed with a production-style workflow: clear separation of concerns, safe configuration handling, and structured outputs from the model.

Features

Gmail OAuth integration (read + draft access)

Email text extraction

Intent classification using a local LLM (Ollama)

Structured JSON outputs from the model

Automatic Gmail draft creation (never sends emails)

Configurable via environment variables

Tech Stack

Python 3

Gmail API

Ollama (phi3)

Requests

python-dotenv

Project Structure
llm-email-assistant/
  src/
    __init__.py
    app.py
    gmail_client.py
    classifier.py
    llm.py
  requirements.txt
  .env.example
  README.md

Setup
1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Install Ollama and pull the model
ollama pull phi3:mini


Ensure Ollama is running:

ollama serve

Gmail API Setup

Create a Google Cloud project

Enable the Gmail API

Create OAuth credentials (Desktop application)

Download the credentials file as credentials.json

Place credentials.json in the project root

credentials.json and generated token.json are intentionally ignored by git.

Configuration

Create your local environment file:

cp .env.example .env


Example variables:

OLLAMA_MODEL=phi3:mini
GMAIL_QUERY=newer_than:7d -category:social -category:promotions
MAX_RESULTS=5

Running the App

From the project root:

python -m src.app


On first run, a browser window will open to authorise Gmail access.

Safety Notes

This project does not send emails

It only creates draft replies

All LLM inference runs locally via Ollama

No email content is sent to external services

Future Improvements

Rule-based pre-filtering before LLM calls

needs_reply vs informational separation

SQLite persistence to avoid reprocessing emails

CLI flags (--dry-run, --max-results)

Evaluation dataset for classification quality

License

This project is for educational and portfolio purposes.
