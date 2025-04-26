"""Helper fn for converting row into articles"""

import pandas as pd

from src.api.database.models.articles import Articles


def convert_to_article(row: pd.Series) -> Articles:
    """converts a `pd.Series` (row) into an `Articles` model
    :param row: from a loop through the df"""

    category = row["category"]
    title = row["title"]
    content = row["content"]
    return Articles(category=category, title=title, content=content)
