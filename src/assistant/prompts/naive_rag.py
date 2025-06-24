"""
very naive prompt
"""

RAG_PROMPT = """
Using the information contained in the context, give a comprehensive answer to the question.
If the answer cannot be deduced from the context, do not give an answer.

Context:
{% for doc in documents %}
Document id {{doc.id}}, title: {{doc.meta.title}}: {{ doc.content }}
{% endfor %}

Question: {{query}}

Response format:
- Provide your answer based on the context
- Provide all the documents that you used, that you got from the context along with their id and title,  in a formatted way to showcase the sources you got.
"""
