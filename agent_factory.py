# agent_factory.py

import streamlit as st
from customer_support_agent import load_support_docs, build_retriever, create_agent

def get_user_agent(username, orders):
    if "retriever" not in st.session_state:
        support_docs = load_support_docs("docs")
        st.session_state.retriever = build_retriever(support_docs)
    if "user_agents" not in st.session_state:
        st.session_state.user_agents = {}
    if username not in st.session_state.user_agents:
        # Each agent is tied to retriever and per-user orders
        st.session_state.user_agents[username] = create_agent(st.session_state.retriever, orders)
    return st.session_state.user_agents[username]
