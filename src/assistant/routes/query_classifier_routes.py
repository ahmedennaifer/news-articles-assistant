"""
The route used to route each query to its category
this just matches each output type to the relevant pipeline
"""

from haystack.dataclasses import ChatMessage, Document

ChatMessage.from_user
routes = [
    {
        "condition": '{{"ToolQuery" in replies[0]}}',
        "output": "{{query}}",
        "output_name": "tool_query",
        "output_type": str,
    },
    {
        "condition": '{{"RAGQuery" in replies[0]}}',
        "output": "{{query}}",
        "output_name": "rag_query",
        "output_type": str,
    },
    {
        "condition": '{{"DBQuery" in replies[0]}}',
        "output": "{{query}}",
        "output_name": "db_query",
        "output_type": str,
    },
    {
        "condition": "{{'GeneralQAQuery' in replies[0]}}",
        "output": "{{query}}",
        "output_name": "general_query",
        "output_type": str,
    },
    {
        "condition": "{{True}}",
        "output": "{{query}}",
        "output_name": "error",
        "output_type": str,
    },
]
