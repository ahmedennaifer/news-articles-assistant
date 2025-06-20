"""benchmarker class for creating the eval dataset"""

from benchmarks.data.questions import test_questions
from typing import List
from haystack import Document
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", 20)
pd.set_option("display.precision", 2)


class Benchmarker:
    NUM_QUESTIONS = 33

    def __init__(
        self, ground_truth_csv_path: str = "benchmarks/data/samples.csv"
    ) -> None:
        self._path = ground_truth_csv_path
        self._ground_truth = self._prepare_ground_truth()
        self.df = self._create_df()

    def _prepare_ground_truth(self) -> List[List[Document]]:
        df = pd.read_csv(self._path)

        #  mapping from title to content, fixes bug from np.repeat
        doc_map = {}
        for _, row in df.iterrows():
            title = row["title"]
            content = row["content"]
            doc_map[title] = content

        question_to_doc_mapping = [
            # Questions 1-3: Lord Scarman
            "Lord Scarman  93  dies peacefully",
            "Lord Scarman  93  dies peacefully",
            "Lord Scarman  93  dies peacefully",
            # Questions 4-6: Council tax
            "Council tax rise 'reasonable'",
            "Council tax rise 'reasonable'",
            "Council tax rise 'reasonable'",
            # Questions 7-9: McConnell
            "McConnell details Scots wave toll",
            "McConnell details Scots wave toll",
            "McConnell details Scots wave toll",
            # Questions 10-12: Casino Royale
            "Casino Royale is next Bond movie",
            "Casino Royale is next Bond movie",
            "Casino Royale is next Bond movie",
            # Questions 13-15: Ring of Fire
            "Ring of Fire hit co-writer dies",
            "Ring of Fire hit co-writer dies",
            "Ring of Fire hit co-writer dies",
            # Questions 16-18: Bortolami
            "Bortolami predicts dour contest",
            "Bortolami predicts dour contest",
            "Bortolami predicts dour contest",
            # Questions 19-21: iTunes
            "ITunes user sues Apple over iPod",
            "ITunes user sues Apple over iPod",
            "ITunes user sues Apple over iPod",
            # Questions 22-24: Broadband
            "Broadband in the UK growing fast",
            "Broadband in the UK growing fast",
            "Broadband in the UK growing fast",
            # Questions 25-27: BMW
            "BMW reveals new models pipeline",
            "BMW reveals new models pipeline",
            "BMW reveals new models pipeline",
            # Questions 28-30: House prices
            "House prices suffer festive fall",
            "House prices suffer festive fall",
            "House prices suffer festive fall",
            # Questions 31-33: Gold
            "Gold falls on IMF sale concerns",
            "Gold falls on IMF sale concerns",
            "Gold falls on IMF sale concerns",
        ]

        ground_truth_docs = []
        for doc_title in question_to_doc_mapping:
            if doc_title in doc_map:
                content = doc_map[doc_title]
                ground_truth_docs.append([Document(content=content)])
            else:
                raise ValueError(f"Document '{doc_title}' not found in CSV")

        return ground_truth_docs

    def _create_df(self) -> pd.DataFrame:
        llm_response = ["" for _ in range(self.NUM_QUESTIONS)]
        return pd.DataFrame(
            {
                "question": test_questions,
                "ground_truth": self._ground_truth,
                "llm_response": llm_response,
            }
        )

    def populate_with_llm_response(self, llm_responses: List[str]) -> pd.DataFrame:
        self.df["llm_response"] = llm_responses
        return self.df

    def __call__(self) -> pd.DataFrame:
        return self.df
