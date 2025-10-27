import os
from langchain.chat_models import init_chat_model

if "GOOGLE_API_KEY" not in os.environ:
    raise RuntimeError("GOOGLE_API_KEY environment variable is required")

if "DATABASE_URI" not in os.environ:
    raise RuntimeError("DATABASE_URI environment variable is required")


google_model = init_chat_model(
    temperature=1,
    model_provider="google_genai",
    model="gemini-2.5-flash",
)

db_uri = os.environ["DATABASE_URI"]