import json
from datetime import datetime
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROFILE_DIR = "profiles"

def profile_path(username):
    return os.path.join(PROFILE_DIR, f"{username}.json")

def load_user_profile(username):
    os.makedirs(PROFILE_DIR, exist_ok=True)
    path = profile_path(username)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {
        "username": username,
        "preferences": {
            "test_framework": "unittest",
            "indent_style": "    ",
            "docstring_format": "google",
        },
        "bookmarks": [],
        "notes": []
    }

def save_user_profile(profile):
    os.makedirs(PROFILE_DIR, exist_ok=True)
    with open(profile_path(profile['username']), "w") as f:
        json.dump(profile, f, indent=2, default=str)

def bookmark(profile, query, answer):
    profile["bookmarks"].append({
        "query": query,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })
    print(profile)
    save_user_profile(profile)

def add_note(profile, note):
    profile["notes"].append({
        "note": note,
        "timestamp": datetime.now().isoformat()
    })
    save_user_profile(profile)
