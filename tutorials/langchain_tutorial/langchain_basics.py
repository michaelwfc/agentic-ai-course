from utils.env_utils import load_env, get_env
from utils.qwen_api import init_langchain_chat_openai
from langchain_core.messages import HumanMessage, SystemMessage, AIMessageChunk

def run_langchain_chat_model():
    """https://docs.langchain.com/oss/python/integrations/chat/tongyi
    """
    
    chat_model = init_langchain_chat_openai()

    # Create messages
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Who are you?")
    ]

    # Get response
    response = chat_model.invoke(messages)
    # print(response.content)
    return response
  

def run_streaming():
    chat_model = init_langchain_chat_openai()

    # Create messages
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Who are you?")
    ]

    # Get response
    response_generator = chat_model.stream(messages)
    for index, chunk in enumerate(response_generator):
        print(f"Chunk {index}:")
        print(chunk.content, end="\n", flush=True)
        
        
  
if __name__ == "__main__":
  load_env()

  # response = run_langchain_chat_model()
  # print(response)
  
  run_streaming()