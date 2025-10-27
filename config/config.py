import getpass
import os
from langchain.chat_models import init_chat_model

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


google_model = init_chat_model(
    temperature=1,
    model_provider="google_genai",
    model="gemini-2.5-flash"
)