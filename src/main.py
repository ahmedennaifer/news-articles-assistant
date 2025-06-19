"""entry point that groups all pipelines"""

from assistant.pipelines.main_pipeline import run_main_pipe


def main() -> None:
    """testing"""

    while True:
        query = input("Ask your question").strip()
        print("Thinking...")
        run_main_pipe(queries=[query])


if __name__ == "__main__":
    main()
