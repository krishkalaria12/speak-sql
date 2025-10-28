from langchain.messages import HumanMessage
from langgraph.types import Command, interrupt

from state import MessagesState

def human_node(state: MessagesState):
    """Human Intervention node - loops back to model unless input is done"""

    last_message = state["messages"][-1].content

    user_feedback = interrupt(
        {
            "message": last_message
        }
    )

    human_response = str(user_feedback)

    human_message = HumanMessage(content=human_response)

    return Command(
        update={
            "messages": [human_message],
            "user_details": [human_message],
            "user_message": human_response,
            "awaiting_user_input": False
        },
        goto="book_ticket"
    )
