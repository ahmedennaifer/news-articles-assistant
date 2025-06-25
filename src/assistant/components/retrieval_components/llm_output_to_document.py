from typing import List

from haystack import component
from haystack import Document


@component
class LLMOutputToDocument:
    """class for the custom component"""

    @component.output_types(documents=List[Document])
    def run(self, messages: List[str]):
        """converts a list of strings input into a Document"""
        return {"documents": [Document(content=message) for message in messages]}
