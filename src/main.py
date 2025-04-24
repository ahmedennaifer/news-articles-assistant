"""entry point that groups all pipelines"""

from assistant.pipelines.main_pipeline import run_main_pipe


def main() -> None:
    """testing"""

    tool_query = "What is the weather today in berlin?"
    rag_query = "What does the paper on biology talk about?"
    db_query = "Can you show me the first lines of our database?"
    web_search_query = "What is the approval rate for trump currently?"

    queries = [web_search_query, rag_query, tool_query, db_query]

    print(f"running main pipe for queries: {queries}...")
    run_main_pipe(queries=queries)


if __name__ == "__main__":
    main()
