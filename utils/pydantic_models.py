from pydantic import BaseModel

class ChatItemRequest(BaseModel):
    question: str
    chat_history: list[tuple]


class ChatItemResponse(BaseModel):
    response_message: str
    chat_history: list[tuple]


