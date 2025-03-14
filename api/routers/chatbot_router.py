import logging

from fastapi import APIRouter

from api.dependencies import hermes_service
from api.schemas.chat_schemas import ChatResp, ChatReq

logger = logging.getLogger(__name__)
chatbot_router = APIRouter(prefix='/chatbot')


@chatbot_router.post("/chat", tags=["chatbot"])
async def chat(
        chat_req: ChatReq,
) -> ChatResp:
    """
    Chat with the chatbot
    :param chat_req: the chat request
    :return: the chat response
    """
    chat_id = chat_req.chat_id
    message = chat_req.message
    response = hermes_service.chat(user_message=message, chat_id=chat_id)
    return ChatResp(
        chat_id=chat_id,
        message=response,
   )
