"""not working, returns score of 0.0, should prob do custom mrr"""

import time

from typing import Dict, List
from haystack import Document, Pipeline
from haystack.components.embedders.hugging_face_api_text_embedder import (
    HuggingFaceAPITextEmbedder,
)
from haystack.components.evaluators import DocumentMRREvaluator
from haystack.utils import Secret
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from src.assistant.vectordb.db import get_doc_store

from benchmarks.benchmark import Benchmark

# ERROR/TODO : returns list of [0,0,0,0,0..]
# IMPORTANT:


def evaluation_pipeline(
    ground_truth_documents: List[List[Document]],
    retrieved_documents: List[List[Document]],
) -> List[Dict[str, float]]:
    pipeline = Pipeline()
    mrr_evaluator = DocumentMRREvaluator()
    pipeline.add_component("mrr_evaluator", mrr_evaluator)
    result = pipeline.run(
        {
            "mrr_evaluator": {
                "ground_truth_documents": ground_truth_documents,
                "retrieved_documents": retrieved_documents,
            },
        }
    )
    return [result[evaluator] for evaluator in result]


def retrieval_pipeline(store, query: str) -> List[Document]:
    text_embedder = HuggingFaceAPITextEmbedder(
        api_type="serverless_inference_api",
        api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
        token=Secret.from_env_var("HF_KEY"),
    )
    retriever = QdrantEmbeddingRetriever(store, top_k=5)
    pipe = Pipeline()
    pipe.add_component("retriever", retriever)
    pipe.add_component("text_embed", text_embedder)
    pipe.connect("text_embed.embedding", "retriever.query_embedding")
    res = pipe.run({"text_embed": {"text": query}})
    return res["retriever"]["documents"]


if __name__ == "__main__":
    bench = Benchmark()

    retrieved_documents = []
    for question in bench.df.question:
        retrieved_documents.append(
            retrieval_pipeline(get_doc_store(collection_name="testing"), question)
        )
        time.sleep(0.5)

    """
    df = question, ground, llm
    -> fill llm col
    """
    df = bench.populate_with_llm_response(retrieved_documents)
    df.to_csv("test_df.csv")
