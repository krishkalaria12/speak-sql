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

    return Command(
        update={
            "user_details": state["user_details"] + [user_feedback]
        }, 
        goto="book_ticket"
    )
