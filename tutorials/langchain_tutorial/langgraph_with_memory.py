import asyncio
import os
from typing import TypedDict, Literal, Annotated
from operator import add
from pydantic import BaseModel, Field, field_validator, ValidationError
import sqlite3
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.errors import InvalidUpdateError
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    AnyMessage,
    RemoveMessage,
)
from langgraph.graph.message import MessagesState, add_messages

from configs.db_config import DB_PATH
from utils.env_utils import load_env
from utils.langchain_utils import save_graph_image
from utils.qwen_api import init_langchain_chat_openai


class PydanticState(BaseModel):
    name: str
    # mood: str = Field(..., description="The mood of the person, either 'happy' or 'sad'")

    # @field_validator('mood')
    # @classmethod
    # def validate_mood(cls, value):
    #     # Ensure the mood is either "happy" or "sad"
    #     if value not in ["happy", "sad"]:
    #         raise ValueError("Each mood must be either 'happy' or 'sad'")
    #     return value

    # mood: Literal["happy", "sad"] = Field(..., description="The mood of the person, either 'happy' or 'sad'")


def run_pydantic_state():
    try:
        state = PydanticState(name="John Doe", mood="mad")
    except ValidationError as e:
        print("Validation Error:", e)


class SimpleState(TypedDict):
    foo: Annotated[list[int], add]


def node_1(state):
    print("---Node 1---")
    return {"foo": [state["foo"][-1] + 1]}


def node_2(state):
    print("---Node 2---")
    return {"foo": [state["foo"][-1] + 1]}


def node_3(state):
    print("---Node 3---")
    return {"foo": [state["foo"][-1] + 1]}


def run_simple_graph():

    # Build graph
    builder = StateGraph(SimpleState)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_1", "node_3")
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    # Add
    graph = builder.compile()

    # View
    save_graph_image(graph, filename="simple_graph_v2.png")

    output = graph.invoke({"foo": [1]})
    print(output)


def delete_messages():
    # Message list
    messages = [AIMessage("Hi.", name="Bot", id="1")]
    messages.append(HumanMessage("Hi.", name="Lance", id="2"))
    messages.append(
        AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3")
    )

    new_message = HumanMessage(
        "Yes, I know about whales. But what others should I learn about?",
        name="Lance",
        id="4",
    )
    # Test
    messages = add_messages(messages, new_message)

    # Isolate messages to delete
    delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]]
    print(delete_messages)
    output_messages = add_messages(messages, delete_messages)


class State(MessagesState):
    summary: str = Field(..., description="The summary of the conversation")


class AgentWithSummary:
    def __init__(self):
        self.llm = init_langchain_chat_openai()
        self.db_path = DB_PATH

        self.memory = MemorySaver()
        # conn = sqlite3.connect(self.db_path, check_same_thread=False)
        # self.memory = SqliteSaver(conn)  
        

    def call_llm_with_summary(self, state: State):
        summary = state.get("summary", "")
        if summary:
            system_message = f"Sumary of conversation history: {summary}\n\n"
            messages = [SystemMessage(content=system_message)] + state["messages"]
        else:
            messages = state["messages"]

        response = self.llm.invoke(messages)
        return {"messages": response}

    def summarize_conversation(self, state: State):

        summary = state.get("summary", "")
        if summary:
            # A summary already exists
            summary_message = (
                f"This is summary of the conversation to date: {summary}\n\n"
                "Extend the summary by taking into account the new messages above:"
            )
        else:
            summary_message = "Create a summary of the conversation above:"
        messages = state["messages"] + [HumanMessage(content=summary_message)]
        response = self.llm.invoke(messages)
        # Delete all but the 2 most recent messages
        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
        return {"summary": response.content, "messages": delete_messages}

    def should_summay(self, state: State) -> Literal["summarize_conversation", END]:
        if len(state["messages"]) > 4:  # Check if there are at least 3 messages
            return "summarize_conversation"
        else:
            return END

    def build_graph_with_summary(self):
        # Build graph
        builder = StateGraph(State)

        builder.add_node("agent", self.call_llm_with_summary)

        builder.add_node("summarize_conversation", self.summarize_conversation)

        builder.add_edge(START, "agent")

        builder.add_conditional_edges("agent", self.should_summay)

        builder.add_edge("summarize_conversation", END)

        graph = builder.compile(checkpointer=self.memory)
        save_graph_image(graph, filename="agent_with_summary.png")
        return graph

    def run(self):
        graph = self.build_graph_with_summary()
        config = {"configurable": {"thread_id": "1"}}

        # Start conversation
        input_message = HumanMessage(content="hi! I'm Lance")
        output = graph.invoke({"messages": [input_message]}, config)
        for m in output["messages"][-1:]:
            m.pretty_print()

        input_message = HumanMessage(content="what's my name?")
        output = graph.invoke({"messages": [input_message]}, config)
        for m in output["messages"][-1:]:
            m.pretty_print()

        input_message = HumanMessage(content="i like the 49ers!")
        output = graph.invoke({"messages": [input_message]}, config)
        for m in output["messages"][-1:]:
            m.pretty_print()

        graph_state = graph.get_state(config)
        print(graph_state)

        summary = graph.get_state(config).values.get(
            "summary", ""
        )  # Access the summary from the graph's state
        print(f"Conversation Summary: {summary}")

    def run_graph_streaming(self, stream_mode="updates"):
        """
        LangGraph supports a few different streaming modes for graph state.

          values: This streams the full state of the graph after each node is called.
          updates: This streams updates to the state of the graph after each node is called.
          
        stream_mode="updates"
        - Because we stream with updates, we only see updates to the state after node in the graph is run.
        - Each chunk is a dict with node_name as the key and the updated state as the value.
        
        Ouptput Example:
        Streaming graph with stream_mode=updates
        ---------------------------------------------------------------------------
        Chunk 0:
        {'agent': {'messages': AIMessage(content="Hi Lance! 👋 It's great to meet you. How can I help you today? Whether it's answering questions, brainstorming ideas, solving a problem, or just having a friendly chat—I'm here for it! 😊", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 47, 'prompt_tokens': 13, 'total_tokens': 60, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen-plus', 'system_fingerprint': None, 'id': 'chatcmpl-edf0ac5b-b1cd-90a0-a652-52ba1aaa2d76', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019d743c-f4c7-72c0-9e09-fe51379af403-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 13, 'output_tokens': 47, 'total_tokens': 60, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})}}
        
        
        
        Streaming graph with stream_mode=values
        ---------------------------------------------------------------------------
        Chunk 0:
        {'messages': [HumanMessage(content="hi! I'm Lance", additional_kwargs={}, response_metadata={}, id='acaa1008-6af9-40b3-b448-e60a37d328c0'), AIMessage(content="Hi Lance! 👋 It's great to meet you. How can I help you today? Whether it's answering questions, brainstorming ideas, solving a problem, or just having a friendly chat—I'm here for it! 😊", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 47, 'prompt_tokens': 13, 'total_tokens': 60, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen-plus', 'system_fingerprint': None, 'id': 'chatcmpl-edf0ac5b-b1cd-90a0-a652-52ba1aaa2d76', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019d743c-f4c7-72c0-9e09-fe51379af403-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 13, 'output_tokens': 47, 'total_tokens': 60, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}), HumanMessage(content="hi! I'm Lance", additional_kwargs={}, response_metadata={}, id='28c63287-6a8d-4dff-b785-6ed7bf993082')]}
        ---------------------------------------------------------------------------
        Chunk 1:
        {'messages': [HumanMessage(content="hi! I'm Lance", additional_kwargs={}, response_metadata={}, id='acaa1008-6af9-40b3-b448-e60a37d328c0'), AIMessage(content="Hi Lance! 👋 It's great to meet you. How can I help you today? Whether it's answering questions, brainstorming ideas, solving a problem, or just having a friendly chat—I'm here for it! 😊", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 47, 'prompt_tokens': 13, 'total_tokens': 60, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen-plus', 'system_fingerprint': None, 'id': 'chatcmpl-edf0ac5b-b1cd-90a0-a652-52ba1aaa2d76', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019d743c-f4c7-72c0-9e09-fe51379af403-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 13, 'output_tokens': 47, 'total_tokens': 60, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}), HumanMessage(content="hi! I'm Lance", additional_kwargs={}, response_metadata={}, id='28c63287-6a8d-4dff-b785-6ed7bf993082'), AIMessage(content="Hi again, Lance! 😊  \nIt looks like your message repeated—did you mean to send something else, or would you like to pick up where we left off? I'm happy to help with anything: tech questions, writing, learning, planning, or even just a lighthearted conversation. Let me know what’s on your mind! 🌟", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 75, 'prompt_tokens': 75, 'total_tokens': 150, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen-plus', 'system_fingerprint': None, 'id': 'chatcmpl-f3649370-b0ef-965e-8deb-97838539d6e2', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--019d7441-a5c6-77e2-aea1-22e8b3fcdfc0-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 75, 'output_tokens': 75, 'total_tokens': 150, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})]}

        
        """
        graph = self.build_graph_with_summary()
        config = {"configurable": {"thread_id": "4"}}

        # Start conversation
        input_message = HumanMessage(content="hi! I'm Lance")
        output = graph.stream(
            {"messages": [input_message]}, config, stream_mode=stream_mode
        )
        print(f"Streaming graph with stream_mode={stream_mode}")
        for index, chunk in enumerate(output):
            print("---"*25)
            print(f"Chunk {index}:")
            print(chunk)
      
      
    async def run_graph_streaming_events(self):
      """
      Streaming tokens
      We often want to stream more than graph state.

      In particular, with chat model calls it is common to stream the tokens as they are generated.

      We can do this using the .astream_events method, which streams back events as they happen inside nodes!

      Each event is a dict with a few keys:

      - event: This is the type of event that is being emitted.
      - name: This is the name of event.
      - data: This is the data associated with the event.
      - metadata: Containslanggraph_node, the node emitting the event.

      The central point is that tokens from chat models within your graph have the on_chat_model_stream type.

      We can use event['metadata']['langgraph_node'] to select the node to stream from.
      And we can use event['data'] to get the actual data for each event, which in this case is an AIMessageChunk

      """
      graph = self.build_graph_with_summary()
      config = {"configurable": {"thread_id": "6"}}
      input_message = HumanMessage(content="hi! I'm Lance")
      events = graph.astream_events(
          {"messages": [input_message]}, config, version="v2"
      )

      node_to_stream = 'agent'
      
      index = 0
      async for event in events:
          print("---" * 25)
          print(f"Event {index}:")
          print(f"Node: {event['metadata'].get('langgraph_node','')}. Type: {event['event']}. Name: {event['name']}")
          
          
          # Get chat model tokens from a particular node 
          # if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node','') == node_to_stream:
          #     data = event["data"]
          #     print(data["chunk"].content, end="|")
          
          print(event)
        
          index += 1


if __name__ == "__main__":
    load_env()
    # print(os.getcwd())
    # run_pydantic_state()

    # run_simple_graph()

    # delete_messages()

    agent = AgentWithSummary()
    # agent.run()
    
    # agent.run_graph_streaming(stream_mode="updates")
    # agent.run_graph_streaming(stream_mode="values")
    
    
    asyncio.run(agent.run_graph_streaming_events())
