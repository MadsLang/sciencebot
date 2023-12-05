from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI, Ollama
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def get_conversational_retriver_chain():
    embeddings_model_name = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=embeddings_model_name
    ) 
    vectorstore = FAISS.load_local('data/faiss_db', embeddings)
    vectorstore.as_retriever(search_type="mmr")

    # Define LLM and retriever model
    llm = OpenAI(temperature=0)
    # llm = Ollama(
    #     model='orca-mini',
    #     base_url="http://localhost:11434",
    #     callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    # )
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

    return ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        max_tokens_limit=4000
    )
