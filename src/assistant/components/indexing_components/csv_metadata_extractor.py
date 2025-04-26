"""custom component that extracts info and populates metadata"""

from haystack import component, Document
from typing import List, Dict
import pandas as pd


@component
class CSVMetadataExtractor:
    """Component that takes a str path and returnes a list of `Document` with metadata"""

    def __init__(self, delimiter=",", header="infer") -> None:
        self.delimiter = delimiter
        self.header = header
        self.docs: List[Document] = []

    def _extract_meta_from_row(self, row: pd.Series) -> Document:
        """extract fields and store as meta
        :param row: `pd.Series` returned from `df.iterrows`
        returns"""
        content = row["content"]
        title = row["title"]
        category = row["category"]
        return Document(content=content, meta={"category": category, "title": title})  # pyright: ignore

    @component.output_types(documents=List[Document])
    def run(self, source: str) -> Dict[str, List[Document]]:
        """entry point of the component
        Note: must always return a dict !
        :param source: path of the csv"""
        df = pd.read_csv(source, delimiter=self.delimiter, header=self.header)  # pyright: ignore
        for _, row in df.iterrows():
            doc = self._extract_meta_from_row(row)
            self.docs.append(doc)
        return {"documents": self.docs}
