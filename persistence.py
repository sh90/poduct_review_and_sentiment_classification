# persistence.py

import json
import os

USER_DB_FILE = "user_db.json"

def save_user_db(user_db):
    """Save the user_db dictionary to a JSON file."""
    with open(USER_DB_FILE, "w") as f:
        json.dump(user_db, f, indent=2)

def load_user_db():
    """Load user_db dictionary from a JSON file. Returns an empty dict if file not found."""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {}
