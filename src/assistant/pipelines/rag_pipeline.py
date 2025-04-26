"""main rag pipeline, still very naive"""

from dotenv import load_dotenv

from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders.hugging_face_api_text_embedder import (
    HuggingFaceAPITextEmbedder,
)
from haystack.utils import Secret
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever

from src.assistant.vectordb.db import get_doc_store
from src.assistant.components.retrieval_components.base_llm import get_base_llm
from src.assistant.prompts.naive_rag import RAG_PROMPT

load_dotenv()


def query_pipeline(store) -> Pipeline:
    """returns the query pipeline, which returns the response of the llm according to the context given by the `store` through the retriver.
    :param store: vector store which stores the embeddings of ours docs"""

    text_embedder = HuggingFaceAPITextEmbedder(
        api_type="serverless_inference_api",
        api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
        token=Secret.from_env_var("HF_KEY"),
    )

    prompt_builder = PromptBuilder(template=RAG_PROMPT, required_variables=["query"])
    retriever = QdrantEmbeddingRetriever(store)
    pipe = Pipeline()
    pipe.add_component("retriever", retriever)
    pipe.add_component("prompt", prompt_builder)
    pipe.add_component("llm", get_base_llm())
    pipe.add_component("text_embed", text_embedder)

    pipe.connect("text_embed.embedding", "retriever.query_embedding")
    pipe.connect("retriever.documents", "prompt.documents")
    pipe.connect("prompt", "llm")
    return pipe


def run_query_pipe(pipe: Pipeline, query: str) -> str:
    """
    runs the query pipeline and formats the response.
    :param pipe: haystack `Pipeline`
    :param query: question of the user
    """
    res = pipe.run({"text_embed": {"text": query}, "prompt": {"query": query}})
    return res["llm"]["replies"][0]
