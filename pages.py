# pages.py

import streamlit as st
from user_data import (
    get_user_profile, save_user_query, add_order
)
from agent_factory import get_user_agent
from persistence import save_user_db
from user_data import escalate_query
from user_data import get_user_profile, resolve_escalation

def login_page():
    st.title("Customer Support Login")
    username = st.text_input("Enter your email (simulated login):")
    if st.button("Login") and username:
        st.session_state["logged_in_user"] = username
        st.success(f"Logged in as {username}")
        st.rerun()

def profile_page(user_profile):
    st.title("My Profile")
    with st.form("profile_form"):
        name = st.text_input("Name", value=user_profile["name"])
        email = st.text_input("Email", value=user_profile["email"], disabled=True)
        phone = st.text_input("Phone", value=user_profile["phone"])
        address = st.text_input("Address", value=user_profile["address"])
        submitted = st.form_submit_button("Update Profile")
        if submitted:
            user_profile.update({"name": name, "phone": phone, "address": address})
            save_user_db(st.session_state.user_db)
            st.success("Profile updated!")
    st.markdown("---")


def history_page(user_history):
    st.title("My Past Queries")
    if user_history:
        for h in reversed(user_history):
            st.markdown(f"<b>Q:</b> {h['query']}<br><b>A:</b> {h['response']}<hr>", unsafe_allow_html=True)

    else:
        st.info("No past queries yet.")

def orders_page(username):
    st.title("My Orders")
    user_orders = get_user_profile(username)["orders"]

    # Add new order (demo purpose)
    with st.form("add_order"):
        item = st.text_input("Item Name", key="order_item")
        submitted = st.form_submit_button("Add Order")
        if submitted and item:
            order = add_order(username, item)
            save_user_db(st.session_state.user_db)
            st.success(f"Order placed! Your Order ID: {order['order_id']}")

    st.subheader("Order History")
    if user_orders:
        for o in reversed(user_orders):
            st.markdown(
                f"<b>Order ID:</b> {o['order_id']}  </br>"
                f"<b>Item:</b> {o['item']} </br>"
                f"<b>Status:</b> {o['status']}  </br>"
                f"<b>Date:</b> {o['date']}  </br>"
            , unsafe_allow_html = True
            )
    else:
        st.info("No orders yet.")

def chat_page(username):
    st.title("Support Chat")
    user_profile = get_user_profile(username)
    orders = user_profile["orders"]
    agent = get_user_agent(username, orders)
    chat_input_key = "chat_input_" + username

    query = st.text_input("Ask a question:", key=chat_input_key)

    if st.button("Send", key="chat_send") and query:
        response = agent.run(query)
        print(response)
        response = response.replace("```","")
        save_user_query(username, query, response)
        save_user_db(st.session_state.user_db)
        del st.session_state[chat_input_key]
        st.rerun()

    history = user_profile["history"]
    for h in reversed(history[-5:]):
        # Escalate button for each answer
        st.markdown(f"<b>Q:</b> {h['query']}<br><b>A:</b> <span style='font-weight:normal'>{h['response']}</span>", unsafe_allow_html=True)
        if st.button(f"Escalate to Human (for this Q)", key=f"escalate_{h['id']}"):
            escalate_query(username, h['query'], h['response'])
            st.success("Escalation submitted for human review.")

        st.markdown("<hr>", unsafe_allow_html=True)

def escalations_page(username):
    st.title("My Escalations")
    escalations = get_user_profile(username).get("escalations", [])
    if not escalations:
        st.info("No queries escalated yet.")
        return

    for esc in reversed(escalations):
        st.markdown(
            f"<b>Q:</b> {esc['query']}<br>"
            f"<b>A:</b> <span style='font-weight:normal'>{esc['response']}</span><br>"
            f"<b>Status:</b> {esc['status']}",
            unsafe_allow_html=True
        )
        if esc['status'] == "Pending":
            resolution = st.text_input("Human resolution (for demo):", key=f"resolution_{esc['id']}")
            if st.button("Mark as Resolved", key=f"resolve_{esc['id']}"):
                resolve_escalation(username, esc['id'], resolution)
                st.success("Escalation marked as resolved.")
        else:
            st.markdown(f"<b>Resolution:</b> {esc['resolution']}", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
