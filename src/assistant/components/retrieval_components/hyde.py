from __future__ import annotations


from haystack import Pipeline, component, Document
from haystack.components.converters import OutputAdapter
from haystack.components.embedders.hugging_face_api_document_embedder import (
    HuggingFaceAPIDocumentEmbedder,
)

from haystack.components.builders import PromptBuilder

from typing import List
from numpy import array, mean

from haystack.utils import Secret

from src.assistant.components.retrieval_components.base_llm import get_base_llm
from src.assistant.components.retrieval_components.llm_output_to_document import (
    LLMOutputToDocument,
)


@component
class HypotheticalDocumentEmbedder:
    def __init__(
        self,
        nr_completions: int = 5,
        embedder_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.nr_completions = nr_completions
        self.embedder_model = embedder_model
        self.generator = get_base_llm()
        self.prompt_builder = PromptBuilder(
            template="""Given a query, generate a paragraph of text that answers the query.
            query: {{query}}
            Paragraph:
            """,
            required_variables=["query"],
        )

        self.embedder = HuggingFaceAPIDocumentEmbedder(
            api_type="serverless_inference_api",
            api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
            token=Secret.from_env_var("HF_KEY"),
        )

        self.pipeline = Pipeline()
        self.pipeline.add_component(name="prompt_builder", instance=self.prompt_builder)
        self.pipeline.add_component(name="generator", instance=self.generator)
        self.pipeline.add_component(name="embedder", instance=self.embedder)
        self.pipeline.add_component(name="llm_to_doc", instance=LLMOutputToDocument())
        self.pipeline.connect("prompt_builder", "generator")
        self.pipeline.connect("generator.replies", "llm_to_doc.messages")
        self.pipeline.connect("llm_to_doc.documents", "embedder.documents")

    @component.output_types(hyde_embeddings=List[float])
    def run(self, query: str):
        result = self.pipeline.run(data={"prompt_builder": {"query": query}})
        print("result:", result)
        # return a single query vector embedding representing the average of the hypothetical document embeddings
        stacked_embeddings = array(
            [doc.embedding for doc in result["embedder"]["documents"]]
        )
        avg_embeddings = mean(stacked_embeddings, axis=0)
        hyde_vector = avg_embeddings.reshape((1, len(avg_embeddings)))
        return {"hyde_embeddings": hyde_vector[0].tolist()}
