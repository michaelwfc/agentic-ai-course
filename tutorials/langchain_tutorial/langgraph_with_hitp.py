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
from langgraph_basics import multiply, add, divide


class MathAgentWithHITP:
    """
    A math agent with HITP
    """

    def __init__(self):
        self.llm = init_langchain_chat_openai()
        self.tools = [multiply, add, divide]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.sys_msg = SystemMessage(
            content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
        )

        self.memory = MemorySaver()

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
        graph = builder.compile(checkpointer=self.memory, interrupt_before=["tools"])
        save_graph_image(graph, filename="math_agent_with_hitp.png")
        return graph

    def run(self):
        graph = self.build_graph()

        # Input
        initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}
        config = {"configurable": {"thread_id": "t001"}}

        evens = graph.stream(initial_input, config=config, stream_mode="values")
        for event in evens:
            event["messages"][-1].pretty_print()

        state = graph.get_state(config=config)
        print(state)

        user_approval = input("Allow tool use? (y/n): ")
        if user_approval.lower() == "y":
            events = graph.stream(None, config=config, stream_mode="values")
            for event in events:
                event["messages"][-1].pretty_print()
        else:
            print("Tool usage denied.")
            
if __name__ == "__main__":
    load_env()
    agent = MathAgentWithHITP()
    agent.run()
    
