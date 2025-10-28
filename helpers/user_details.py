from langgraph.types import Command, interrupt

from graph import MessagesState

def human_node(state: MessagesState):
    """Human Intervention node - loops back to model unless input is done"""

    message = f"Answer the question asked by the bot, {state["messages"][-1]}"

    user_feedback = interrupt(
        {
            "message": message
        }
    )

    return Command(
        update={
            "user_details": state["user_details"] + [user_feedback]
        }, 
        goto="book_ticket"
    )