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
    query = "Which legislation did Lord Scarman's pioneering work help establish according to Lord Woolf?"
    ground_truth = [
        [
            Document(
                content="Distinguished lawyer Lord Scarman, who conducted the inquiry into the 1981 Brixton riots, has died aged 93.  The peer enjoyed a celebrated judicial career, serving as Law Commission chairman in its first seven years. He also chaired the 1969 tribunal set up to investigate civil disturbances in Northern Ireland. Paying tribute, the Lord Chancellor Lord Falconer said Lord Scarman was one of the great advocates of our generation.  His legacy from his decisions in the Lords and the Court of Appeal is substantial. His work in the wake of the Brixton riots and his commitment to the vulnerable and dispossessed was second to none.  A great judge, a great lawyer and a great man. Lord Scarman's nephew George Ritchie said the peer, who passed away peacefully on Wednesday, would be sadly missed.  The Lord Chief Justice, Lord Woolf, who is the most senior judge in England and Wales, said it was Lord Scarman's pioneering work which paved the way for the Human Rights Act 1998. He was a lawyer and a judge who had a remarkable insight into human nature, and an exceptional sensitivity to the needs of a healthy society, he said. He was, personally, totally charming and he will be remembered with great affection and admiration by all who came into contact with him.  Dame Elizabeth Butler-Sloss, the president of the Family Justice Division, said Lord Scarman was a good and humane judge and one of the greatest figures of the late 20th century. Lord Scarman will be remembered for the public inquiry he led into a string of race riots which began in Brixton when racial tensions rose after a police crackdown on street robbery. During the following three days of disturbances that spread to the Midlands, Merseyside, Bristol and Leeds, nearly 400 people were injured and buildings and vehicles were set alight.  The inquiry famously settled on the so-called rotten apples theory, which argued that only a few police officers were racist, saying most were not. It spawned new law enforcement practices and led to the creation of the Police Complaints Authority. Trevor Phillips, chair of the Commission for Racial Equality, praised Lord Scarman's ability to listen. He said: When Lord Scarman toured the streets of Brixton his presence was electrifying. A community which had been systematically ignored by everyone else was suddenly embraced by the epitome of the English establishment. His great quality was the ability to listen to young people of all backgrounds, many of whose language he could barely understand, genuinely to hear what they had to say and to talk to them as human beings. He never lost the special combination of wisdom, humanity and the spark of radicalism that marked his watershed report into the Brixton riots."  # ruff: ignore
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
