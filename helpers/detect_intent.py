from state import MessagesState
from pydantic import BaseModel, Field
from langchain.messages import SystemMessage, HumanMessage, AIMessage

from config.config import google_model

sys_prompt_detect_intent='''
You are a helpful intent classification assistant for a museum ticketing system. Your role is to analyze user queries and categorize them into one of three types:

**Intent Categories:**
1. **TICKET BOOKING**: User wants to book, purchase, reserve, or inquire about booking museum tickets
   - Examples: "book tickets", "I want to visit tomorrow", "how do I reserve", "can I buy tickets"

2. **MUSEUM INFORMATION**: User wants details about museums (location, hours, exhibits, facilities, pricing info, etc.)
   - Examples: "what museums are available", "opening hours", "where is the museum", "tell me about exhibits"

3. **OUT OF SCOPE**: User is asking about something unrelated to museums or museum tickets

**Instructions:**
- Carefully analyze the user's query to determine their primary intent
- Be flexible and understanding - users may phrase requests in various ways
- For out-of-scope queries, provide a friendly, helpful redirect message that:
  * Acknowledges their query politely
  * Explains what you CAN help with in a positive tone
  * Offers specific examples of questions you can answer
  * Uses a warm, conversational tone (avoid words like "irrelevant" or "invalid")

**Response Structure:**
- If is_museum is true → set is_ticket to false and irrevelant to empty string ""
- If is_ticket is true → set is_museum to false and irrevelant to empty string ""
- If out of scope → set both is_museum and is_ticket to false, and write a friendly redirect message in irrevelant

**Example of a good redirect message:**
"I'm specialized in helping with museum visits and ticketing! While I can't help with flight bookings, I'd be happy to assist you with:
- Finding museums in your area and learning about their exhibits
- Booking tickets for museum visits
- Getting information about opening hours, locations, and pricing

What would you like to know about museums today?"
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
