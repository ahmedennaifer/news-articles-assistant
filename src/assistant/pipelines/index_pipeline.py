"""pipline for storing files into the vector db"""

from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.embedders.hugging_face_api_document_embedder import (
    HuggingFaceAPIDocumentEmbedder,
)
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret

from src.assistant.components.indexing_components.csv_metadata_extractor import (
    CSVMetadataExtractor,
)
from src.assistant.vectordb.db import get_doc_store

load_dotenv()


def index(store, path: str) -> None:
    """
    indexes the documents into a database. Right now, stores in memory and with no pre-processing
    :param store: vector store to store in
    :param path: path of the csv file
    """
    doc_embedder = HuggingFaceAPIDocumentEmbedder(
        api_type="serverless_inference_api",
        api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"},
        token=Secret.from_env_var("HF_KEY"),
    )
    writer = DocumentWriter(store)
    pipe = Pipeline()
    pipe.add_component("converter", CSVMetadataExtractor())
    pipe.add_component("embeder", doc_embedder)
    pipe.add_component("writer", writer)

    pipe.connect("converter", "embeder")
    pipe.connect("embeder", "writer")
    print("running index...")
    pipe.run({"converter": {"source": path}})


def main():
    """indexing runs seperately"""  # TODO: maybe fix
    store = get_doc_store(collection_name="testing")
    index(store, "data/final.csv")


if __name__ == "__main__":
    main()
