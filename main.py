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
        "user_details": []
    }

    for chunk in app.stream(initial_state, config=thread_config):
        for node_id, value in chunk.items():
            if node_id == "__interrupt__":
                user_feedback = input("Enter the details asked by ai: ")
                app.invoke(Command(resume=user_feedback), config=thread_config)
                break

            if node_id == "end_node":
                return


if __name__ == "__main__":
    main()
