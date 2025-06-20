"""Custom MRR Evaluator that compares letters instead of 1to1."""

from typing import Any, Dict, List
from haystack import Document, component


@component
class MRREvaluator:
    """Haystack's mrr does 1to1 comparison, difficult if extra spaces
    or small changes. This mrr does char2char comparison to avoid issues"""

    @staticmethod
    def normalize_content(text: str) -> str:
        """keep only letters"""
        if not text:
            return ""
        return "".join(c.lower() for c in text if c.isalpha())

    @component.output_types(score=float, individual_scores=List[float])
    def run(
        self,
        ground_truth_documents: List[List[Document]],
        retrieved_documents: List[List[Document]],
    ) -> Dict[str, Any]:
        if len(ground_truth_documents) != len(retrieved_documents):
            msg = "length of ground_truth_documents and retrieved_documents must be the same."
            raise ValueError(msg)

        individual_scores = []
        # mrr
        for ground_truth, retrieved in zip(ground_truth_documents, retrieved_documents):
            reciprocal_rank = 0.0

            ground_truth_letters = set()
            for doc in ground_truth:
                if doc.content is not None:
                    letters_only = self.normalize_content(doc.content)
                    ground_truth_letters.add(letters_only)

            for rank, retrieved_document in enumerate(retrieved):
                if retrieved_document.content is None:
                    continue

                retrieved_letters = self.normalize_content(retrieved_document.content)

                if retrieved_letters in ground_truth_letters:
                    reciprocal_rank = 1 / (rank + 1)
                    break

            individual_scores.append(reciprocal_rank)

        score = sum(individual_scores) / len(ground_truth_documents)
        return {"score": score, "individual_scores": individual_scores}
