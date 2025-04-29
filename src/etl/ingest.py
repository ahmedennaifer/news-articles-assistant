"""scripts that write the df into the db"""

import pandas as pd
from tqdm import tqdm

from src.backend.database.db import get_db
from src.etl.helpers.convert_to_article import convert_to_article
from src.etl.helpers.insert_in_db import insert_in_db

# TODO: add logging and remove prints


def main() -> None:
    """main fn, with a loop on all rows, for ease of string formatting"""

    session = get_db()
    df = pd.read_csv("data/final.csv", delimiter=",", header="infer")
    try:
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Adding articles to db"):
            article = convert_to_article(row)
            insert_in_db(article, session=session)
        print(f"done inserting {len(df)} rows")

    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
