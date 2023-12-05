from fastapi import FastAPI
from utils.pydantic_models import ChatItemResponse, ChatItemRequest
from langchain_backend import get_conversational_retriver_chain
from utils.app_helpers_fncs import parse_llm_response
import os

chain = get_conversational_retriver_chain()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.post("/chat/")
async def get_chat(chat_item: ChatItemRequest):
    response_message = chain(
            {
                "question": chat_item.question, 
                "chat_history": chat_item.chat_history
            },
            return_only_outputs=True
    )

    return ChatItemResponse(
        response_message = parse_llm_response(response_message),
        chat_history = [(chat_item.question, response_message["answer"])]
    )
    