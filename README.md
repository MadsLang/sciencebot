# sciencebot
A LLM/RAG application to chat with research papers

*Still under development!*


## How? 

I downloaded a bunch of research papers (only abstract and metadata). From the abstracts, I compute embeddings using SentenceTransformers and store in a local Faiss vectorstore. 

Currently, the frontend and backend have been seperated. The frontend is currently a simple Streamlit app, but I am working on making this into a nicer JS/React. 

Backend is Python - using FastAPI with Langchain. The LLM used is API calls to OpenAI (gpt-3.5-turbo), but I am experimenting with using Ollama to run Llama2 or maybe Mistral models locally. 
