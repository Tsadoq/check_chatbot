from fastapi import FastAPI
from api.routers.chatbot_router import chatbot_router
from api.schemas.generic_schemas import HealthResponse

app = FastAPI()

app.include_router(router=chatbot_router)

@app.get("/health_check", tags=["health_check"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    :return: HealthResponse containing the health status and the current time
    """
    return HealthResponse()