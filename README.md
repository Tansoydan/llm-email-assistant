# LLM Email Assistant (Local)

A local LLM-powered email assistant that connects to Gmail, classifies incoming emails by intent using **Ollama (phi-3)**, and conditionally creates **draft replies** for high-priority messages.

The system is designed to reflect a real production-style workflow: clean project structure, explicit configuration, safe handling of credentials, and structured LLM outputs. All model inference runs **locally**.

---

## Overview

This project demonstrates how a local large language model can be integrated into a real application pipeline rather than used in isolation. The assistant:

- Pulls emails from Gmail via the official API  
- Extracts plain-text content  
- Classifies email intent using a structured LLM prompt  
- Determines whether a response is required  
- Creates Gmail **drafts only** (never sends emails)

---

## Key Features

- Gmail OAuth integration (read + draft permissions)
- Local LLM inference via Ollama (no external LLM APIs)
- Structured JSON classification output
- Configurable Gmail queries
- Safe default behaviour (drafts only)
- Modular, package-based Python layout

---

## Tech Stack

- Python 3  
- Gmail API  
- Ollama (phi-3)  
- requests  
- python-dotenv  

---

## Project Structure

```
llm-email-assistant/
├── src/
│   ├── __init__.py
│   ├── app.py            # Application entry point
│   ├── gmail_client.py   # Gmail API integration
│   ├── classifier.py     # LLM prompt + classification logic
│   └── llm.py            # Ollama client
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Create and activate a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Install Ollama and pull the model

```
ollama pull phi3:mini
```

Ensure Ollama is running:

```
ollama serve
```

---

## Gmail API Setup

1. Create a Google Cloud project  
2. Enable the **Gmail API**  
3. Create OAuth credentials (Desktop application)  
4. Download the credentials file as `credentials.json`  
5. Place `credentials.json` in the project root  

> `credentials.json` and the generated `token.json` are intentionally ignored by git.

---

## Configuration

Create your local environment file:

```
cp .env.example .env
```

Example variables:

```
OLLAMA_MODEL=phi3:mini
GMAIL_QUERY=newer_than:7d -category:social -category:promotions
MAX_RESULTS=5
```

---

## Running the Application

From the project root:

```
python -m src.app
```

On first run, a browser window will open to authorise Gmail access.

---

## Safety Notes

- This project **does not send emails**
- It only creates **draft replies**
- All LLM inference runs locally via Ollama
- No email content is sent to external services

---

## Future Improvements

- Rule-based pre-filtering before LLM calls  
- Separation of "needs_reply" vs informational emails  
- SQLite persistence to avoid reprocessing emails  
- CLI flags (`--dry-run`, `--max-results`)  
- Evaluation dataset for classification quality  

---

## License

This project is intended for educational and portfolio purposes.
