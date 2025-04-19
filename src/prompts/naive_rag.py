"""
very naive prompt
"""

template = """
    Using the information contained in the context, give a comprehensive answer to the question.
    If the answer cannot be deduced from the context, do not give an answer.

    Context:
    {% for doc in documents %}
    {{ doc.content }} 
    {% endfor %};
    Question: {{query}}
    """
