import fastapi
from apps.chat_apis import chat_api
from agents.chat_agents import SimpleChatAgent
import os


def init_app() -> fastapi.FastAPI:
    # Configure timeouts for debugging
    timeout_keep_alive = 300 if os.getenv("FASTAPI_DEBUG") else 30
    timeout_graceful_shutdown = 30 if os.getenv("FASTAPI_DEBUG") else 10
    
    app = fastapi.FastAPI(
        timeout_keep_alive=timeout_keep_alive,
        timeout_graceful_shutdown=timeout_graceful_shutdown
    )
    app.include_router(chat_api)

    @app.on_event("startup")
    async def startup_event():
        # Initialize the chat agent before the server starts handling requests
        app.state.chat_agent = SimpleChatAgent()

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(init_app(), host="0.0.0.0", port=8000)
  