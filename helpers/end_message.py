from state import MessagesState

def end_node(state: MessagesState):
    """Final node"""

    print("Final Response: ", state["messages"][-1].content)
    
    return state