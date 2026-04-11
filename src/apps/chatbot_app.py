import fastapi
from apps.chat_apis import chat_api
from agents.chat_agents import SimpleChatAgent


def init_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    app.include_router(chat_api)

    @app.on_event("startup")
    async def startup_event():
        # Initialize the chat agent before the server starts handling requests
        app.state.chat_agent = SimpleChatAgent()

    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(init_app(), host="0.0.0.0", port=8000)
  