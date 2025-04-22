"""pipline for storing files into the vector db"""

from dotenv import load_dotenv
from haystack import Document, Pipeline
from haystack.components.embedders.hugging_face_api_document_embedder import (
    HuggingFaceAPIDocumentEmbedder,
)
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret

load_dotenv()


def index(store, doc: Document) -> None:
    """
    indexes the documents into a database. Right now, stores in memory and with no pre-processing
    :param store: vector store to store in
    :param doc: any haystack `Document`
    """
    doc_embedder = HuggingFaceAPIDocumentEmbedder(
        api_type="serverless_inference_api",
        api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
        token=Secret.from_env_var("HF_KEY"),
    )
    writer = DocumentWriter(store)
    pipe = Pipeline()
    pipe.add_component("embedder", doc_embedder)
    pipe.add_component("writer", writer)
    pipe.connect("embedder", "writer")
    print("running index...")
    pipe.run({"embedder": {"documents": [doc]}})
