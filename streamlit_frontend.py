import streamlit as st
import requests
import json

### APP MAIN UI

st.title("SCIENCEBOT")
user_name = st.text_input('Your name', 'User')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask me a question about climate research!"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message(user_name):
        st.markdown(prompt)

    with st.chat_message("SCIENCEBOT", avatar="🤖"):
        message_placeholder = st.empty()
        response = ""

        with st.spinner():
            response = requests.post(
                "http://localhost:8000/chat/",
                json={
                    "question": prompt,
                    "chat_history": st.session_state.chat_history,
                }
            )
            response = json.loads(response.text)

            st.session_state.chat_history += response['chat_history']

        message_placeholder.markdown(
            response["response_message"],
            unsafe_allow_html=True
        )
    
    st.session_state.messages.append({"role": "SCIENCEBOT", "content": response['response_message']})
