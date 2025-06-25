"""evaluation script"""

import time

from typing import Dict, List
from haystack import Document, Pipeline
from haystack.components.embedders.hugging_face_api_text_embedder import (
    HuggingFaceAPITextEmbedder,
)
from haystack.utils import Secret
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack_integrations.components.rankers.cohere.ranker import CohereRanker

from src.assistant.prompts.metadata_labeller import metadata_labeller_prompt
from src.assistant.components.retrieval_components.metadata_labeller import (
    MetadataLabeller,
)
from src.assistant.vectordb.db import get_doc_store

from benchmarks.benchmark import Benchmarker

from src.assistant.components.evaluation_components.mrr_evaluator import MRREvaluator


def evaluation_pipeline(
    ground_truth_documents: List[List[Document]],
    retrieved_documents: List[List[Document]],
) -> Dict[str, float]:
    pipeline = Pipeline()
    mrr_evaluator = MRREvaluator()
    pipeline.add_component("mrr_evaluator", mrr_evaluator)
    result = pipeline.run(
        {
            "mrr_evaluator": {
                "ground_truth_documents": ground_truth_documents,
                "retrieved_documents": retrieved_documents,
            },
        }
    )
    return result["mrr_evaluator"]


def retrieval_pipeline(store, query: str) -> List[Document]:
    text_embedder = HuggingFaceAPITextEmbedder(
        api_type="serverless_inference_api",
        api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
        token=Secret.from_env_var("HF_KEY"),
    )
    retriever = QdrantEmbeddingRetriever(store, top_k=5)
    ranker = CohereRanker(top_k=5)
    pipe = Pipeline()
    pipe.add_component("retriever", retriever)
    pipe.add_component("text_embed", text_embedder)
    pipe.add_component("ranker", ranker)
    pipe.add_component("metadata_labeller", MetadataLabeller(metadata_labeller_prompt))

    pipe.connect("text_embed.embedding", "retriever.query_embedding")
    pipe.connect("metadata_labeller.filters", "retriever.filters")
    pipe.connect("retriever.documents", "ranker.documents")

    res = pipe.run(
        {
            "text_embed": {"text": query},
            "metadata_labeller": {"query": query},
            "ranker": {"query": query},
        }
    )
    return res["ranker"]["documents"]


if __name__ == "__main__":
    bench = Benchmarker()

    retrieved_documents = []
    for question in bench.df.question:
        retrieved_documents.append(
            retrieval_pipeline(get_doc_store(collection_name="testing2"), question)
        )
        time.sleep(10)

    result = evaluation_pipeline(bench._ground_truth, retrieved_documents)

    print(f"MRR: {result['score']}")
    print(f"individual MRR: {result['individual_scores']}")
