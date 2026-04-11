


from typing import List,Dict, Text

from langchain_core.messages import (
    SystemMessage,
    AIMessage,
    HumanMessage,
    AnyMessage,
    ToolMessage,
)
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver


from utils.env_utils import load_env
from utils.qwen_api import init_langchain_chat_openai
from utils.langchain_utils import save_graph_image
from tools.calculator_tools import calculator, calculator_wstate
# from langgraph_basics import multiply, add, divide

load_env()


class SimpleChatAgent():

    def __init__(self):
        self.filename="simple_chatbot.png"
        self.llm = init_langchain_chat_openai()
        # self.tools = [multiply, add, divide]
        self.tools = [calculator]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.sys_msg = SystemMessage(
            content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
        )

        self.memory = MemorySaver()
        self.graph = self.build_graph()

    def call_llm_with_tools(self, state: MessagesState):
        responese = self.llm_with_tools.invoke([self.sys_msg] + state["messages"])
        return {"messages": [responese]}

    def build_graph(self) -> CompiledStateGraph:

        builder = StateGraph(MessagesState)
        builder.add_node("agent", self.call_llm_with_tools)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "agent")
        builder.add_conditional_edges("agent", tools_condition)

        builder.add_edge("tools", "agent")
        # The breakpoints are set during compile time.
        # A checkpointer is required to enable breakpoints.
        graph = builder.compile(checkpointer=self.memory, interrupt_before=["tools"])
        save_graph_image(graph, filename=self.filename)
        return graph
      
    def get_last_message(self,thread_id:str)-> Text:
        config = {"configurable": {"thread_id": thread_id}}
        state = self.graph.get_state(config)
        content = state.values["messages"][-1].content
        return content
      
    

    def run(self,messages:List[Dict[Text,Text]],thread_id:Text="t001")-> Text:
        
        config = {"configurable": {"thread_id": thread_id}}
        
        # Input
        message = messages[-1]["content"]
        initial_input = {"messages": HumanMessage(content=message)}
        
        # --- Step 1: Run until interrupt (before tools node) ---
          
        events = self.graph.stream(initial_input, config=config, stream_mode="values")

        for event in events:
            event["messages"][-1].pretty_print()

        # --- Step 2: Check if graph is interrupted ---
        snapshot = self.graph.get_state(config)
        if snapshot.next and "tools" in snapshot.next:
          
            # Graph is paused before tools — ask user
            user_approval = input("Allow tool use? (y/n): ")

            if user_approval.lower() == "y":
                # --- Step 3a: Resume by passing None (continue from checkpoint) ---
                events = self.graph.stream(None, config=config, stream_mode="values")
                for event in events:
                    event["messages"][-1].pretty_print()
            else:
                # --- Step 3b: Reject — inject a ToolMessage to cancel gracefully ---
                current_state = self.graph.get_state(config)
                last_message = current_state.values["messages"][-1]
                tool_call_id = last_message.tool_calls[0]["id"]

                self.graph.update_state(
                    config,
                    {
                        "messages": [
                            ToolMessage(
                                content="Tool usage denied by user. Do not answer this question.",
                                tool_call_id=tool_call_id,
                            )
                        ]
                    },
                    as_node="tools",  # pretend tools node ran
                )
                # Resume so agent can respond to the denial
                events = self.graph.stream(None, config=config, stream_mode="values")
                for event in events:
                    event["messages"][-1].pretty_print()
                    
            reponse = event["messages"][-1].content
            return reponse
          
    
    def run_until_approval(self, messages:List[Dict[Text,Text]],thread_id:Text="t001")-> bool:

        config = {"configurable": {"thread_id": thread_id}}
        message = messages[-1]["content"]
        initial_input = {"messages": HumanMessage(content=message)}
        events = self.graph.stream(initial_input, config=config, stream_mode="values")
        for event in events:
            event["messages"][-1].pretty_print()
            
        snapshot = self.graph.get_state(config)
        if snapshot.next and "tools" in snapshot.next:
          return True
        return False
      
    def resume(self,approved:bool,thread_id:Text="t001")-> Text:
        
        config = {"configurable": {"thread_id": thread_id}}
        if approved:
          events = self.graph.stream(None, config=config, stream_mode="values")
          for event in events:
            event["messages"][-1].pretty_print()
        else:
          state = self.graph.get_state(config)
          last_message = state.values["messages"][-1]
          tool_call_id = last_message.tool_calls[0]["id"]
          self.graph.update_state(
              config,
              {
                  "messages": [
                      ToolMessage(
                          content="Tool usage denied by user. Do not answer this question.",
                          tool_call_id=tool_call_id,
                      )
                  ]
              },
              as_node="tools",  # pretend tools node ran
          )
          events = self.graph.stream(None, config=config, stream_mode="values")
          for event in events:
            event["messages"][-1].pretty_print()
            

        response = self.get_last_message(thread_id)
        return response

            
                    
          
            
            
if __name__ == "__main__":
    load_env()
    agent = SimpleChatAgent()
    
    messages = [
        {"role": "user", "content": "I want to add 2 and 3"},
    ]
    reponse = agent.run(messages=messages)
    print(f"Reponse: {reponse}")
    