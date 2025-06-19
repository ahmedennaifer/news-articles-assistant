"""entry point that groups all pipelines"""

from assistant.pipelines.main_pipeline import run_main_pipe


def main() -> None:
    """testing"""
    query = ""
    while query != "exit":
        query = input("Ask your question\n > ")
        print("Thinking...\n")
        run_main_pipe(queries=[query])
    print("Exiting...")


if __name__ == "__main__":
    main()
