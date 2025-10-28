from langchain.messages import HumanMessage
from langgraph.types import Command

from graph import thread_config, app

def main():
    user_input = input("Enter your query: ")
    initial_state = {
        "messages": [
            HumanMessage(
                content=user_input
            )
        ],
        "user_message": user_input,
        "to_book_or_detail": False,
        "irrevelant_question": "",
        "user_details": [],
        "awaiting_user_input": False
    }

    state = initial_state
    should_continue = True

    while should_continue:
        interrupted = False
        for chunk in app.stream(state, config=thread_config):
            for node_id, value in chunk.items():
                if node_id == "__interrupt__":
                    interrupt = value[0] if isinstance(value, (list, tuple)) and value else value
                    payload = getattr(interrupt, "value", interrupt)
                    if isinstance(payload, dict):
                        ai_question = payload.get("message", "Enter the details asked by ai: ")
                    elif payload is None:
                        ai_question = "Enter the details asked by ai: "
                    else:
                        ai_question = str(payload)

                    print(f"\n{ai_question}")
                    user_feedback = input("-> ")

                    interrupt_id = getattr(interrupt, "id", None)
                    resume_payload = {interrupt_id: user_feedback} if interrupt_id else user_feedback

                    # Resume the graph execution
                    app.invoke(Command(resume=resume_payload), config=thread_config)
                    # Set state to None to continue streaming from checkpoint
                    state = None
                    interrupted = True
                    break

                if node_id == "end_node":
                    should_continue = False
                    break

                if isinstance(value, dict) and "messages" in value:
                    messages = value["messages"]
                    if isinstance(messages, list) and messages:
                        last_message = messages[-1]
                        if last_message.__class__.__name__ == "AIMessage":
                            print(f"\n{last_message.content}")

            # Break out of chunk loop if we hit an interrupt or end
            if interrupted or not should_continue:
                break

        # If we completed streaming without an interrupt, we're done
        if not interrupted:
            should_continue = False


if __name__ == "__main__":
    main()
