import json
from pathlib import Path

SESSION_FILE = Path("session_state.json")

def load_session():
    if SESSION_FILE.exists():
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_session(data: dict):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def reset_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
