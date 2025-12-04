from typing import Dict, Any

# In-memory store (resets when server restarts)
STUDENT_PREFERENCES: Dict[int, Dict[str, Any]] = {}

def save_preferences(user_id: int, data: dict):
    STUDENT_PREFERENCES[user_id] = data

def get_preferences(user_id: int):
    return STUDENT_PREFERENCES.get(user_id)
