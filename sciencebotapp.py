from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
import os
from credentials import openai_key
from utils.app_helpers_fncs import parse_llm_response
import streamlit as st

# Set API KEY
os.environ['OPENAI_API_KEY'] = openai_key


# Load vectorstore
msg = st.toast("Loading model...")
st.session_state.embeddings_model_name = "sentence-transformers/all-mpnet-base-v2"
st.session_state.embeddings = HuggingFaceEmbeddings(
    model_name=st.session_state.embeddings_model_name
) 
msg.toast("Loading database...")
st.session_state.vectorstore = FAISS.load_local('data/faiss_db', st.session_state.embeddings)
st.session_state.vectorstore.as_retriever(search_type="mmr")

# Define LLM and retriever model
msg.toast("Still loading...")
st.session_state.llm = OpenAI(temperature=0)
st.session_state.question_generator = LLMChain(llm=st.session_state.llm, prompt=CONDENSE_QUESTION_PROMPT)
st.session_state.doc_chain = load_qa_with_sources_chain(st.session_state.llm, chain_type="map_reduce")

msg.toast("Almost there...")
st.session_state.chain = ConversationalRetrievalChain(
    retriever=st.session_state.vectorstore.as_retriever(),
    question_generator=st.session_state.question_generator,
    combine_docs_chain=st.session_state.doc_chain,
    max_tokens_limit=4000
)
msg.toast('Ready to chat!', icon = "🎉")


### APP MAIN UI

# 
st.title("SCIENCEBOT")
user_name = st.text_input('Your name', 'User')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me a question about climate research!"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message(user_name):
        st.markdown(prompt)

    with st.chat_message("SCIENCEBOT", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner():
            full_response = st.session_state.chain(
                {
                    "question": prompt, 
                    "chat_history": st.session_state.chat_history
                }, 
                return_only_outputs=True
            )

            st.session_state.chat_history = [(prompt, full_response["answer"])]

        message_placeholder.markdown(
            parse_llm_response(full_response),
            unsafe_allow_html=True
        )
    
    st.session_state.messages.append({"role": "SCIENCEBOT", "content": full_response['answer']})

