"""qdrant doc store"""

from haystack_integrations.document_stores.qdrant import QdrantDocumentStore


def get_doc_store(collection_name: str) -> QdrantDocumentStore:
    """get qdrant store"""
    return QdrantDocumentStore(
        url="http://qdrant:6333",
        index=collection_name,
        embedding_dim=384,
        use_sparse_embeddings=False,
    )
