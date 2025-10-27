from langchain.tools import tool

from helpers.query_checker import check_query
from helpers.get_db import get_db

@tool
def read_db(query):
    '''
        This is the tool to call the db and read the values from it,
        we will be having only 2 table which includes ticket booking and museum details
        You can search for records in the table using the tool 
        for example: Searching the record for the user john doe on the date 28/10/25 for the time 4:00pm

        Args:
            Query: string
        
        You need to pass the Query to fetch the records from the db
        Do not send any query which harms the user records and tables
    '''

    # check with llm for the rightfulness of the query
    isSafe = check_query(query)

    if not isSafe:
        return "The query given by you is not safe to read the records. Try again with some other query"
    
    # send the uri
    db = get_db()
    query_ans = db.run(query)

    return query_ans