from pydantic import BaseModel, Field


class ChatReq(BaseModel):
    chat_id: str = Field(
        ...,
        title="Chat ID",
        description="The ID of the chat",
        examples=["1234567890"]
    )
    message: str = Field(
        ...,
        title="Message",
        description="The message to send",
        examples=["How can I get slack notifications?"]
    )

class ChatResp(BaseModel):
    chat_id: str = Field(
        ...,
        title="Chat ID",
        description="The ID of the chat",
        examples=["1234567890"]
    )
    message: str = Field(
        ...,
        title="Message",
        description="The response message",
        examples=["You can get slack notifications by following these steps..."]
    )
