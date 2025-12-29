from typing_extensions import TypedDict
from typing import Annotated, List
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from agents.react_agents import react_agent, tools


class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


def agent_node(state: State):
    result = react_agent.invoke(state)
    return {"messages": result["messages"]}


builder = StateGraph(State)

builder.add_node("agent", agent_node)
# builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
# builder.add_conditional_edges("agent", tools_condition)
# builder.add_edge("tools", "agent")
builder.add_edge("agent", END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
