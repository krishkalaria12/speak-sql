from langchain.tools import tool

from helpers.query_checker import check_query
from helpers.get_db import get_db
from config.config import db_uri

@tool
def write_and_update_db(query: str) -> str:
    """
    Write and update database queries for the allowed application tables.
    Description:
        Constructs or modifies SQL queries intended for safe execution against the
        application's permitted tables (e.g., ticket_booking and museum_details).
        The function validates the provided SQL with a safety check before attempting
        execution and only executes queries that pass the validation.
    Parameters:
        query (str): The SQL statement or snippet to be written/edited. This can be a
                     full command (SELECT, INSERT, UPDATE) or a partial query to be
                     completed and validated.
    Returns:
        str: The result returned by the database client when the validated query is
             executed (e.g., rows, rows-affected message) or an explanatory message
             when the query is rejected for safety reasons.
    Allowed operations:
        - Safe reads: SELECT queries that do not leak sensitive data.
        - Inserts: INSERT statements to add new records to the allowed tables.
        - Updates: UPDATE statements that modify records in the allowed tables,
                   preferably with well-scoped WHERE clauses.
    Disallowed or restricted operations:
        - Destructive schema/data commands such as DROP, DELETE, TRUNCATE, ALTER,
          or any command that removes tables or broadly deletes data are not allowed
          by default.
        - Queries that attempt to access or exfiltrate sensitive fields, credentials,
          or data outside the permitted tables are disallowed.
    Safety and confirmation policy:
        - Every query is first checked with an automated safety validator (e.g., check_query).
          If the query is flagged as unsafe, it will not be executed and an explanatory
          message will be returned.
        - For sensitive commands (for example DELETE, DROP, TRUNCATE, ALTER or other
          destructive operations), you strictly need to ask the user about it before
          proceeding. The tool must request explicit, informed confirmation from the user
          (clearly describing the risk and the exact effect) prior to constructing or
          executing any such command.
        - The tool will never autonomously execute commands that modify schema or perform
          irreversible data loss without affirmative user confirmation.
    Usage guidance / examples:
        - Build an INSERT to add a new ticket booking record.
        - Edit an UPDATE to narrow a WHERE clause to a single record.
        - Compose a SELECT to read museum details while respecting privacy constraints.
    Implementation notes:
        - Validation is performed prior to database access (e.g., check_query(query, "write")).
        - Database execution is performed via the configured DB client (e.g., get_db(db_uri).run(query)).
        - If the safety check fails, the function returns a clear error/guidance message and does not run the query.
    """
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
    isSafe = check_query(query, "write")

    if not isSafe:
        return "The query given by you is not safe to write or update the records. Try again with some other query"
    
    # send the uri
    db = get_db(db_uri)
    query_ans = db.run(query)

    return query_ans