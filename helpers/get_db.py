from langchain_community.utilities import SQLDatabase

def get_db(uri):
    db = SQLDatabase.from_uri(
        uri
    )

    return db