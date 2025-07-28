import streamlit as st
import requests

st.set_page_config(page_title="AML Regulation Chat", layout="wide")
st.title("💬 Ask Anti Money Laundering (AML) Regulation")

# initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about AML Regulation"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # with st.chat_message("user"):
    st.markdown(
    f"""
    <div style='text-align: right;'>
    <div style='display: inline-block; background-color: #0059b3; color: white; padding: 10px 15px; border-radius: 15px; max-width: 70%; word-wrap: break-word;'>
    {prompt}
    </div>
    </div>
     """,
    unsafe_allow_html=True,
     )                                                                                 

    with st.chat_message("assistant"):
        with st.spinner("Searching AML Regulations..."):
            response = requests.post(
                "http://localhost:8000/ask", params={"query": prompt}
            )
            if response.status_code == 200:
                answer = response.json()["response"]
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            else:
                st.error("❌ Failed to get response from backend.")
