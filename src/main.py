from pipelines.rag_pipeline import query, index
from components.query_classifier import get_query_classifier_pipeline
from haystack.components.routers import ConditionalRouter
from haystack import SuperComponent
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Pipeline, Document


# TODO: rag_query -> rag_pipeline
# TODO: db_query -> db_tool
# TODO: generalQuery -> normal generator
# TODO: tool_query -> tool
# TODO: tool_query + db query -> tool-using agent


rag_paragraph = "A groundbreaking paper published in the Journal of Molecular Biology explores the intricate relationship between mitochondrial function and cellular aging. The researchers utilized advanced microscopy techniques to observe real-time changes in mitochondrial morphology as cells progress through their life cycle. Their findings suggest that specific proteins regulating mitochondrial fusion and fission play a crucial role in determining cellular lifespan, potentially offering new targets for age-related disease interventions. What makes this study particularly noteworthy is its novel approach to tracking individual mitochondria over extended periods, revealing previously unobserved patterns of deterioration that precede cellular senescence. The implications extend beyond basic research, pointing toward potential therapeutic strategies that could modify these pathways to promote cellular health and longevity in aging populations"


def main():
    routes = [
        {
            "condition": '{{"ToolQuery" in replies[0]}}',
            "output": "{{query}}",
            "output_name": "tool_query",
            "output_type": str,
        },
        {
            "condition": '{{"RAGQuery" in replies[0]}}',
            "output": "{{query}}",
            "output_name": "rag_query",
            "output_type": str,
        },
        {
            "condition": '{{"DBQuery" in replies[0]}}',
            "output": "{{query}}",
            "output_name": "db_query",
            "output_type": str,
        },
        {
            "condition": "{{'GeneralQAQuery' in replies[0]}}",
            "output": "{{query}}",
            "output_name": "general_query",
            "output_type": str,
        },
        {
            "condition": "{{True}}",
            "output": "{{query}}",
            "output_name": "error",
            "output_type": str,
        },
    ]
    store = InMemoryDocumentStore()
    index(store, Document(content=rag_paragraph))
    query_pipe = query(store)
    router = ConditionalRouter(routes)
    pipe = Pipeline()
    superComponent = get_query_classifier_pipeline()
    pipe.add_component("router", router)
    pipe.add_component("classifier", superComponent)

    pipe.add_component(
        "rag_pipe",
        SuperComponent(
            query_pipe,
            input_mapping={
                "query": ["text_embed.text", "prompt.query"],
            },
        ),
    )
    pipe.connect("classifier.replies", "router.replies")
    pipe.connect("router.rag_query", "rag_pipe.query")

    tool_query = "Can you query our endpoints and analyze the logs?"
    rag_query = "What does the paper on biology talk about?"
    db_query = "What are our regional sales for Q4?"
    general_query = "What is the capital of Paris?"
    queries = [tool_query, rag_query, db_query, general_query]

    for q in queries:
        result = pipe.run(
            {
                "classifier": {"query": q},
                "router": {"query": q},
            }
        )
        print(result)


if __name__ == "__main__":
    main()
