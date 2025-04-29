"""not working, returns score of 0.0, should prob do custom mrr"""

from typing import Dict, List
from haystack import Document, Pipeline
from haystack.components.embedders.hugging_face_api_text_embedder import (
    HuggingFaceAPITextEmbedder,
)
from haystack.components.evaluators import DocumentMRREvaluator
from haystack.utils import Secret
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from src.assistant.vectordb.db import get_doc_store


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
    query = "What was the specific athletic event in which Kelly Holmes won her Olympic gold medal that was voted as the top television moment of 2004, and which other sports moments did this victory surpass in the BBC poll?"
    ground_truth = [
        [
            Document(
                content="Sprinter Kelly Holmes' Olympic victory has been named the top television moment of 2004 in a BBC poll.  Holmes' 800m gold medal victory beat favourite moments from drama, comedy and factual programmes, as voted by television viewers. Natasha Kaplinsky's Strictly Come Dancing win was top entertainment moment and a Little Britain breast feeding sketch won the comedy prize. The 2004 TV Moments will be shown on BBC One at 2000 GMT on Wednesday. Double gold medal winner Holmes topped the best sports moment category, beating Maria Sharapova's Wimbledon triumph and Matthew Pinsent's rowing victory at the Olympics.  She then went on to take the overall prize of Golden TV Moment. The sight of former royal correspondent Jennie Bond with dozens of rats crawling over her in ITV's I'm a Celebrity Get Me Out of Here was named best factual entertainment moment. Michael Buerk's return to Ethiopia, 20 years after originally reporting its famine, topped the factual category for BBC programme This World. Long-running soap EastEnders won the best popular drama moment title when character Dot confided in Den Watts that she was unwell."
            )
        ],
    ]
    retrieved_documents = [
        retrieval_pipeline(get_doc_store(collection_name="testing"), query)
    ]
    print(len(ground_truth), len(retrieved_documents))
    print("ground: ", ground_truth)
    print("------------------------------------------")
    print("retrieved: ", retrieved_documents)
    print("------------------------------------------")
    res = evaluation_pipeline(ground_truth, retrieved_documents)
    print("results:", res)

