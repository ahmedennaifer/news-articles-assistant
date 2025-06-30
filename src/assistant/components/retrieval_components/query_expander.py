import json

from typing import List, Optional

from haystack import Pipeline, component
from haystack.components.builders import PromptBuilder

from src.assistant.components.retrieval_components.base_llm import get_base_llm


@component
class QueryExpander:
    def __init__(self, prompt: Optional[str] = None):
        self.query_expansion_prompt = prompt
        if prompt is None:
            self.query_expansion_prompt = """
          You are part of an information system that processes users queries.
          You expand a given query into {{ number }} queries that are similar in meaning.

          Structure:
          Follow the structure shown below in examples to generate expanded queries.
          Examples:
          1. Example Query 1: "climate change effects"
          Example Expanded Queries: ["impact of climate change", "consequences of global warming", "effects of environmental changes"]

          2. Example Query 2: ""machine learning algorithms""
          Example Expanded Queries: ["neural networks", "clustering", "supervised learning", "deep learning"]

          Your Task:
          Query: "{{query}}"
          Example Expanded Queries:
          """
        builder = PromptBuilder(self.query_expansion_prompt)
        llm = get_base_llm()
        self.pipeline = Pipeline()
        self.pipeline.add_component(name="builder", instance=builder)
        self.pipeline.add_component(name="llm", instance=llm)
        self.pipeline.connect("builder", "llm")

    @component.output_types(queries=List[str])
    def run(self, query: str, number: int = 5):
        result = self.pipeline.run({"builder": {"query": query, "number": number}})
        expanded_query = json.loads(result["llm"]["replies"][0]) + [query]
        return {"queries": list(expanded_query)}
