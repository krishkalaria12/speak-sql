from pydantic import BaseModel, Field
from config.config import google_model

sys_prompt_query_read = '''
You are an SQL expert and a helpful assistant. Check whether the given SQL query is harmless and only reads records from the database (read-only).
Return a structured JSON containing a single boolean field "safe".

- "safe": true  -> query is read-only (examples: SELECT, SHOW, DESCRIBE, EXPLAIN).
- "safe": false -> query modifies data or schema (examples: INSERT, UPDATE, DELETE, CREATE, ALTER, DROP) or otherwise is unsafe for read-only purposes.

Examples:
    SELECT * FROM users LIMIT 5;                      -> {"safe": true}
    SHOW TABLES;                                      -> {"safe": true}
    INSERT INTO employees (...) VALUES (...);         -> {"safe": false}
    UPDATE users SET name='x' WHERE id=1;            -> {"safe": false}
    DROP TABLE users;                                 -> {"safe": false}

Answer ONLY the structured JSON object, with no extra commentary.
'''

sys_prompt_query_write_and_update = '''
You are an SQL expert and a helpful assistant. Check whether the given SQL query is a write/modify operation (i.e., it will change data or schema).
Return a structured JSON containing a single boolean field "safe".

- "safe": true  -> query writes/modifies data or schema (examples: INSERT, UPDATE, DELETE, MERGE, CREATE, ALTER, DROP).
- "safe": false -> query is read-only or otherwise does not perform writes (examples: SELECT, SHOW, DESCRIBE, EXPLAIN).

Examples:
    INSERT INTO employees (id, name) VALUES (1, 'John'); -> {"safe": true}
    UPDATE users SET email='a@b.com' WHERE id=2;          -> {"safe": true}
    DELETE FROM orders WHERE id=10;                       -> {"safe": true}
    CREATE TABLE t (id INT);                              -> {"safe": true}
    SELECT * FROM users LIMIT 1;                          -> {"safe": false}

Answer ONLY the structured JSON object, with no extra commentary.
'''

class Safety(BaseModel):
    '''Safety of the query to read records'''
    safe: bool = Field(..., description="Is the query safe for reading records from the table")

def check_query(query, mode):
    messages = [
        {
            "role": "system",
            "content": sys_prompt_query_read if mode=="read" else sys_prompt_query_write_and_update
        },
        {
            "role": "user",
            "content": query
        }
    ]

    model_with_structure = google_model.with_structured_output(Safety)
    response = model_with_structure.invoke(messages)
    
    return response.safe
