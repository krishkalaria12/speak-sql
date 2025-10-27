from langchain.tools import tool

from helpers.query_checker import check_query
from helpers.get_db import get_db

@tool
def write_and_update_db(query):
    '''
        This tool helps write and edit the prompt (SQL query) before it's validated and executed.
        Use it to construct or modify queries for the two tables: ticket booking and museum details.
        Examples:
            - Build an INSERT or UPDATE to add or change records.
            - Edit a WHERE clause to refine which records are read or updated.
        Args:
            query: str - the SQL query or prompt to write/edit.
        Notes:
            - Do not create queries that drop or delete tables or expose sensitive data.
            - Only generate safe read/insert/update queries for the allowed tables.
    '''

    # check with llm for the rightfulness of the query
    isSafe = check_query(query)

    if not isSafe:
        return "The query given by you is not safe to write or update the records. Try again with some other query"
    
    # send the uri
    db = get_db()
    query_ans = db.run(query)

    return query_ans