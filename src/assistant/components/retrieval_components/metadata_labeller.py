from haystack import component, Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from src.assistant.components.retrieval_components.base_llm import get_base_llm

from typing import Dict
# tech, sport, business, enterntainement, politics


@component
class MetadataLabeller:
    """takes query -> filters"""

    def __init__(self, prompt):
        self.llm = get_base_llm()
        self.pipeline = Pipeline()
        self.prompt = prompt
        self.prompt_builder = PromptBuilder(self.prompt, required_variables=["query"])
        self._setup_pipeline()

    def _setup_pipeline(self) -> None:
        self.pipeline.add_component("llm", self.llm)
        self.pipeline.add_component("prompt_builder", self.prompt_builder)
        self.pipeline.connect("prompt_builder", "llm")

    @component.output_types(filters=Dict[str, str])
    def run(self, query):
        result = self.pipeline.run({"prompt_builder": {"query": query}})

        field = result["llm"]["replies"][0]
        return {
            # "operator": "AND",
            "conditions": [
                {"field": "meta.category", "operator": "==", "value": field},
            ],
        }
