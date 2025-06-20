"""entry point that groups all pipelines"""

from src.assistant.pipelines.main_pipeline import run_main_pipe
import time


def main() -> None:
    """testing"""
    try:
        while True:
            query = input("Ask your question\n > ")
            print("Thinking...\n")
            run_main_pipe(queries=[query])
    except KeyboardInterrupt:
        print("\nBye!")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
