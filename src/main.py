from components.query_classifier import get_query_classifier_pipeline
from haystack.components.routers import ConditionalRouter
from haystack import Pipeline, component


def main():
    routes = [
        {
            "condition": '{{"ToolQuery" in replies[0]}}',
            "output": "{{replies}}",
            "output_name": "tool_query",
            "output_type": str,
        },
        {
            "condition": '{{"RAGQuery" in replies[0]}}',
            "output": "{{replies}}",
            "output_name": "rag_query",
            "output_type": str,
        },
        {
            "condition": '{{"DBQuery" in replies[0]}}',
            "output": "{{replies}}",
            "output_name": "db_query",
            "output_type": str,
        },
        {
            "condition": "{{'GeneralQAQuery' in replies[0]}}",
            "output": "{{replies}}",
            "output_name": "general_query",
            "output_type": str,
        },
        {
            "condition": "{{True}}",
            "output": "{{replies}}",
            "output_name": "error",
            "output_type": str,
        },
    ]
    router = ConditionalRouter(routes)
    pipe = Pipeline()
    superComponent = get_query_classifier_pipeline()
    pipe.add_component("router", router)
    pipe.add_component("classifier", superComponent)
    pipe.connect("classifier.replies", "router.replies")

    tool_query = "Can you query our endpoints and analyze the logs?"
    rag_query = "What does the paper on biology talk about?"
    db_query = "What are our regional sales for Q4?"
    general_query = "What is the capital of Paris?"
    queries = [tool_query, rag_query, db_query, general_query]
    for query in queries:
        result = pipe.run({"classifier": {"query": query}})
        result_list = list(result.get("router", {}).keys())
        fmt_router_response = result_list
        print(fmt_router_response)


if __name__ == "__main__":
    main()
