from benchmarks.data.questions import test_questions

from typing import List
from haystack import Document

import numpy as np
import pandas as pd

"""
make a df with ground vs predicted
should be of form:
question, ground_truth, ai_response
"""

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", 20)
pd.set_option("display.precision", 2)


class Benchmark:
    NUM_QUESTIONS = 33  # 33 questions in our eval set

    def __init__(
        self, ground_truth_csv_path: str = "benchmarks/data/samples.csv"
    ) -> None:
        self._path = ground_truth_csv_path
        self._ground_truth = self._prepare_ground_truth()
        self.df = self._create_df()

    def _prepare_ground_truth(self) -> List[List[Document]]:
        old = pd.read_csv(self._path)
        raw_ground_truth = old["content"].to_list()
        res = self._format_ground_truth(raw_ground_truth)
        return [[Document(content=str(cnt))] for cnt in res]

    def _create_df(self) -> pd.DataFrame:
        llm_response = ["" for _ in range(self.NUM_QUESTIONS)]
        return pd.DataFrame(
            {
                "question": test_questions,
                "ground_truth": self._ground_truth,
                "llm_response": llm_response,
            }
        )

    def _format_ground_truth(self, raw_ground_truth: List[str]):
        """for samples, each entry has 3 questions.
        we need to map each 3 questions -> each sample"""
        # repeat the ground truth  3 times to match 3 questions
        return np.repeat(raw_ground_truth, 3)

    def populate_with_llm_response(self, llm_responses: List[str]) -> pd.DataFrame:
        self.df["llm_response"] = llm_responses
        return self.df

    def __call__(self) -> pd.DataFrame:
        return self.df
