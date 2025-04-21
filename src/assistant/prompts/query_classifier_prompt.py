"""prompt for classfying the query. With few-shots"""

QUERY_CLASSIFIER_PROMPT = """You are tasked of categorizing a user's query into 4 categories:
You are tasked of categorizing a user's query into 4 categories:
- RAGQuery: A very specific and direct query that can be found through search techniques of a certain corpus. these are generally questions that can only be answered through a certain expertise.
- DBQuery: A query that needs to talk to a relational database. For example, how much does item B cost?
- ToolQuery: A query that can be answered by a number of tools. These are queries that needs something to get done, or ask about something that can be acquired through APIs. A tool is a python function. 
            such as: - Make an entry to google calendar 
                     - What is the weather today?
                     - What is the current time?
                     - And any other query that needs to use the concept of a tool.
- GeneralQAQuery: A query than can be answered by an LLM's training data. These are very general query, like what is the capital of Paris, and such.
You need to always respond with this format, and this format only. No other output is tolerated: 
     {"category": "RAGQuery", "query": query}
     {"category": "DBQuery", "query": query}
     {"category": "GeneralQAQuery", "query": query}
     {"category": "ToolQuery", "query": query}
Here is the query you need to classify: {{query}}
"""
