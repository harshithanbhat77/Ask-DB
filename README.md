# Chat-QnA

A small Python project for creating a chat / Q&A interface that integrates SQL tools and prompt templates.

This repository contains utilities and custom prompt construction for SQL-related retrieval and query generation.

## Repository layout

- `custom_sql_prompt.py` — custom prompt definitions and templates.
- `custom_sql_toolkit.py` — (tooling for SQL interactions)
- `ollama_sql.py` — (OLLAMA model integration helpers)
- `session_manager.py` — session handling utilities.
- `config.py` — configuration variables used by the project.
- `requirements.txt` — Python dependencies.

## Prerequisites

- Python 3.10+ recommended.
- A virtual environment (highly recommended).
- Windows PowerShell (these instructions use PowerShell commands).

## Setup (PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you prefer, install `langchain` or other packages individually (the code expects LangChain-style imports).

## Quick usage

This project is a collection of modules rather than a single script. Typical usage is:

- Import the prompt and toolkit modules from your own script or REPL.

Example (interactive):

```powershell
# activate venv as above
python -c "from custom_sql_prompt import SOME_SYMBOL; print('imports OK')"
```

Replace `SOME_SYMBOL` with an exported name from `custom_sql_prompt.py` you intend to use.

## Troubleshooting / Common fixes

- "PromptTemplate is not defined" — add the LangChain import at the top of the file:

```python
from langchain.prompts import PromptTemplate
```

- "Import langchain.tools.retriever could not be resolved" — this usually means the project's LangChain version or layout differs from the code's imports. Try one of:
  - Inspect `requirements.txt` and install the version pinned there.
  - Replace non-existent imports with the current LangChain equivalents (consult LangChain docs).

## Next steps (suggested)

- Add a minimal runnable example script `examples/run_chat.py` that demonstrates end-to-end usage with a small SQLite dataset.
- Add tests for prompt construction (unit tests).
- Add a short CONTRIBUTING.md and license if this will be shared.

## Contact / Notes

This README is intentionally minimal. If you want, I can:

- Create an `examples/run_chat.py` example and a small SQLite fixture.
- Inspect `requirements.txt` and update the README to explicitly document the versions used.

---

(Generated automatically)