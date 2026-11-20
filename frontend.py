"""Streamlit frontend interface for AI Financial Advisor Bot."""

import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="AI Financial Advisor Bot", page_icon="💰")
st.title("AI Financial Advisor Bot")

# Expander listing recent handoffs
with st.expander("Recent Handoffs", expanded=False):
    try:
        resp = requests.get(f"{BACKEND_URL}/handoffs", timeout=120)
        if resp.status_code == 200:
            handoffs = resp.json()
            if handoffs:
                for h in reversed(handoffs):
                    st.markdown(
                        f"**{h.get('timestamp', '')}**: `{h.get('from_agent')} ➔ {h.get('to_agent')}`  \n"
                        f"- **Reason:** {h.get('reason')}  \n"
                        f"- **Context:** {h.get('context')}"
                    )
                    st.divider()
            else:
                st.write("No handoffs recorded yet.")
        else:
            st.error(f"Error fetching handoffs: {resp.status_code}")
    except Exception as err:
        st.warning(f"Could not load handoffs: {err}")

# Chat message history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("answered_by"):
            st.caption(f"Answered by: **{msg['answered_by']}**")
        if msg.get("handoff"):
            h = msg["handoff"]
            st.info(
                f"**Handoff:** {h.get('from')} ➔ {h.get('to')}  \n"
                f"**Reason:** {h.get('reason')}  \n"
                f"**Context:** {h.get('context')}"
            )

# Chat input box
if prompt := st.chat_input("Ask a financial question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking (the backend might be waking up)..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": prompt},
                    timeout=120,
                )
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "")
                    answered_by = data.get("answered_by", "Unknown")
                    handoff_info = data.get("handoff")

                    st.markdown(answer)
                    st.caption(f"Answered by: **{answered_by}**")
                    if handoff_info:
                        st.info(
                            f"**Handoff:** {handoff_info.get('from')} ➔ {handoff_info.get('to')}  \n"
                            f"**Reason:** {handoff_info.get('reason')}  \n"
                            f"**Context:** {handoff_info.get('context')}"
                        )
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "answered_by": answered_by,
                            "handoff": handoff_info,
                        }
                    )
                else:
                    st.error(f"Backend error ({res.status_code}): {res.text}")
            except Exception as err:
                st.error(f"Request failed: {err}")
