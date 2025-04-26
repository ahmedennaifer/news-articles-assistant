"""ChatMessage converter component"""

from typing import List

from haystack import component
from haystack.dataclasses import ChatMessage


@component
class StringToChatMessage:
    """class for the custom component"""

    @component.output_types(messages=List[ChatMessage])
    def run(self, messages: str):
        """converts a string input into a `ChatMessage`format that is expected for agent messages"""
        return {"messages": [ChatMessage.from_user(messages)]}
