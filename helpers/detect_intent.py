from state import MessagesState
from pydantic import BaseModel, Field
from langchain.messages import SystemMessage, HumanMessage, AIMessage

from config.config import google_model

sys_prompt_detect_intent='''
    You are an helpful assistant who decides whether the question is of the 2 type. the first type is the booking ticket and the second question is of the type museum details. You need to decide whether the user query is asking for which type.
    and if the user query is irrevelant, you need to respond to it with a proper answer for example: the asked question is irrevelant. try asking for something related to museum details or ask them to book the tickets for the museum

    You need to answer in a structured response 
    if is_museum is true then is_ticket is false and irrevelant is empty string ""
    if is_ticket is true then is_museum is false and 
    if irrevelant question then write the response then is_museum is false and is_ticker is false
'''

class DetectIntent(BaseModel):
    '''Detect the intent of the user'''
    is_ticket: bool = Field(..., description="Is the user asking to book ticket")
    is_museum: bool = Field(..., description="Is the user asking for more details of the museum")
    irrevelant: str = Field(..., description="Is the user asking to book ticket")

def detect_intent(state: MessagesState):
    user_message = state.get("user_message")

    messages = [
        SystemMessage(
            content=sys_prompt_detect_intent
        ),
        HumanMessage(
            content=user_message
        )
    ] + state["messages"]

    # call the llm
    model_with_structure = google_model.with_structured_output(DetectIntent)
    response = model_with_structure.invoke(messages)

    if response.is_ticket:
        state["to_book_or_detail"] = True
        state["irrevelant_question"] = ""
        return state

    if response.is_museum:
        state["to_book_or_detail"] = False
        state["irrevelant_question"] = ""
        return state

    state["irrevelant_question"] = response.irrevelant
    state["messages"] = state["messages"] + [AIMessage(content=response.irrevelant)]

    return state
