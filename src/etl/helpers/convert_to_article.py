"""Helper fn for converting row into articles"""

import pandas as pd

from src.backend.database.models.article import Article


def convert_to_article(row: pd.Series) -> Article:
    """converts a `pd.Series` (row) into an `Articles` model
    :param row: from a loop through the df"""

    category = row["category"]
    title = row["title"]
    content = row["content"]
    return Article(category=category, title=title, content=content)
