from langchain.messages import AnyMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
import operator

from helpers.detect_intent import detect_intent
from helpers.route_query import routeQuery

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_message: str
    # to book ticket -> true, museum -> false
    to_book_or_detail: bool
    irrevelant_question: str

# Build the workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("detect_intent", detect_intent)


# Add edges to connect nodes
agent_builder.add_edge(START, "detect_intent")
agent_builder.add_conditional_edges(
    "detect_intent",
    routeQuery,
    {
        "irrevelant": END,
        "museum": "", # to be implemented
        "ticket": ""
    }
)