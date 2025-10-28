from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_message: str
    # to book ticket -> true, museum -> false
    to_book_or_detail: bool
    irrevelant_question: str
    user_details: Annotated[list[AnyMessage], operator.add]
