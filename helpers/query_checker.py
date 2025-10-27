from pydantic import BaseModel, Field
from config.config import google_model

sys_prompt_query_read='''
    You are an sql expert and a helpful assisstant who checks whether the query is a harmless query and query is only to read the records from the table instead of creating or updating the records in the table
    You need to inform it by a boolean value for the variable safe.
    Example:
        1. SELECT * FROM users LIMIT 5; -> SAFE=true
        2. INSERT INTO employees (id, first_name, last_name, email, hire_date)
VALUES (1, 'John', 'Doe', 'johndoe@example.com', '2025-10-27');
-> SAFE=false

    ANSWER THE QUERY IN STRUCTURED RESPONSE
'''

class Safety(BaseModel):
    '''Safety of the query to read records'''
    safe: bool = Field(..., description="Is the query safe for reading records from the table")

def check_query(query):
    messages = [
        {
            "role": "system",
            "content": sys_prompt_query_read
        },
        {
            "role": "user",
            "content": query
        }
    ]

    model_with_structure = google_model.with_structured_output(Safety)
    response = model_with_structure.invoke(messages)
    
    return response.safe
