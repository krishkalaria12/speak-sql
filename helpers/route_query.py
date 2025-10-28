from state import MessagesState

def routeQuery(state: MessagesState):
    """Gate function to route the query which includes book ticket or get museum detail or irrelevant question based on the user query"""

    if state["irrevelant_question"]:
        return "irrevelant"
    if state["to_book_or_detail"]:
        return "ticket"

    return "museum"
