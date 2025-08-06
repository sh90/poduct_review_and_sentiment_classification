# user_data.py

import streamlit as st
import uuid
from persistence import save_user_db

def get_user_profile(username):
    db = st.session_state.user_db
    if username not in db:
        db[username] = {
            "profile": {"name": "", "email": username, "phone": "", "address": ""},
            "history": [],
            "orders": []
        }
        save_user_db(st.session_state.user_db)
    return db[username]

def save_user_query(username, query, response):
    st.session_state.user_db[username]["history"].append({
        "id": str(uuid.uuid4()),
        "query": query,
        "response": response
    })
    save_user_db(st.session_state.user_db)

def add_order(username, item, status="Processing"):
    order = {
        "order_id": str(uuid.uuid4())[:8],
        "item": item,
        "status": status,
        "date": "2025-08-06"
    }
    st.session_state.user_db[username]["orders"].append(order)
    save_user_db(st.session_state.user_db)
    return order

def escalate_query(username, query, response):
    db = st.session_state.user_db
    if "escalations" not in db[username]:
        db[username]["escalations"] = []
    escalation = {
        "id": str(uuid.uuid4()),
        "query": query,
        "response": response,
        "status": "Pending",
        "resolution": ""
    }
    db[username]["escalations"].append(escalation)
    from persistence import save_user_db
    save_user_db(st.session_state.user_db)

def resolve_escalation(username, escalation_id, resolution):
    db = st.session_state.user_db
    if "escalations" not in db[username]:
        return
    for esc in db[username]["escalations"]:
        if esc["id"] == escalation_id:
            esc["status"] = "Resolved"
            esc["resolution"] = resolution
            break
    from persistence import save_user_db
    save_user_db(st.session_state.user_db)

