from langchain.messages import AnyMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.checkpoint.memory import MemorySaver
import uuid

from helpers.detect_intent import detect_intent
from helpers.route_query import routeQuery
from helpers.get_museum_details import get_museum_details
from helpers.book_ticket import book_ticket
from helpers.user_details import human_node
from helpers.end_message import end_node

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_message: str
    # to book ticket -> true, museum -> false
    to_book_or_detail: bool
    irrevelant_question: str
    user_details: Annotated[list[AnyMessage], operator.add]

# Build the workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("detect_intent", detect_intent)
agent_builder.add_node("get_museum_details", get_museum_details)
agent_builder.add_node("book_ticket", book_ticket)
agent_builder.add_node("human_node", human_node)
agent_builder.add_node("end_node", end_node)

agent_builder.set_entry_point("detect_intent")

# Add edges to connect nodes
agent_builder.add_edge(START, "detect_intent")
agent_builder.add_conditional_edges(
    "detect_intent",
    routeQuery,
    {
        "irrevelant": "end_node",
        "museum": "get_museum_details",
        "ticket": "book_ticket"
    }
)
agent_builder.add_edge("get_museum_details", "end_node")
agent_builder.add_edge("book_ticket", "human_node")
agent_builder.add_edge("end_node", END)

agent_builder.set_finish_point("end_node")

# Enable Interrupt mechanism
checkpointer = MemorySaver()
app = agent_builder.compile(checkpointer=checkpointer)

thread_config = {"configurable": {
    "thread_id": uuid.uuid4()
}}