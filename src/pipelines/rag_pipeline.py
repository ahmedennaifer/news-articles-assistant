"""main rag pipeline, still very naive"""

from dotenv import load_dotenv
from haystack import Document, Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders.hugging_face_api_text_embedder import (
    HuggingFaceAPITextEmbedder,
)
from haystack.components.generators.openai import OpenAIGenerator
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.utils import Secret

from src.pipelines.index_pipeline import index
from src.prompts.naive_rag import template

load_dotenv()


RAG_PARAGRAPH = "A groundbreaking paper published in the Journal of Molecular Biology explores the intricate relationship between mitochondrial function and cellular aging. The researchers utilized advanced microscopy techniques to observe real-time changes in mitochondrial morphology as cells progress through their life cycle. Their findings suggest that specific proteins regulating mitochondrial fusion and fission play a crucial role in determining cellular lifespan, potentially offering new targets for age-related disease interventions. What makes this study particularly noteworthy is its novel approach to tracking individual mitochondria over extended periods, revealing previously unobserved patterns of deterioration that precede cellular senescence. The implications extend beyond basic research, pointing toward potential therapeutic strategies that could modify these pathways to promote cellular health and longevity in aging populations"


def query_pipeline(store) -> Pipeline:
    """returns the query pipeline, which returns the response of the llm according to the context given by the `store` through the retriver.
    :param store: vector store which stores the embeddings of ours docs"""

    text_embedder = HuggingFaceAPITextEmbedder(
        api_type="serverless_inference_api",
        api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
        token=Secret.from_env_var("HF_KEY"),
    )

    llm = OpenAIGenerator(
        api_key=Secret.from_env_var("GROQ_KEY"),
        api_base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
        generation_kwargs={"max_tokens": 512},
    )

    prompt_builder = PromptBuilder(template=template, required_variables=["query"])
    retriever = InMemoryEmbeddingRetriever(store)
    pipe = Pipeline()
    pipe.add_component("retriever", retriever)
    pipe.add_component("prompt", prompt_builder)
    pipe.add_component("llm", llm)
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


def main():
    """testing"""
    store = InMemoryDocumentStore()
    rag_query = "What does the paper on biology talk about?"
    index(store, Document(content=RAG_PARAGRAPH))
    pipe = query_pipeline(store)
    llm_answer = run_query_pipe(pipe, rag_query)
    print(llm_answer)


if __name__ == "__main__":
    main()
