"""tool that lets an agents write stuff to the db"""

from typing import Any

from haystack.tools import Tool
from sqlalchemy import text
from src.api.database.db import get_db

READ_FROM_DB_TOOL_PARAMS = {
    "type": "object",
    "properties": {"sql": {"type": "string"}},
    "required": ["sql"],
}


def _read_from_db(sql) -> Any:
    """executes raw sql into the db. very bad, and unsanitized"""  # TODO: rewrite better
    _session = get_db()
    hits = _session.execute(statement=text(sql)).fetchall()
    return hits


def read_from_db_tool(tool_params: dict = READ_FROM_DB_TOOL_PARAMS) -> Tool:
    """returns a formatted Tool object"""
    return Tool(
        name="read_from_db_tool",
        description="""This tool fetches data from the database through sql queries, \n
        you need to provide the sql according to the schema provided.
        (the table is a collection of bbc articles with this format :
                    ( articles (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL, 
                    category VARCHAR NOT NULL, 
                    content TEXT NOT NULL) ), questions can be like: \n 
                    how many times is the word "usa" mentionned?, how many articles have the title "peace" etc...""",
        parameters=tool_params,
        function=_read_from_db,
    )
