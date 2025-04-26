"""helper function for writing an article into the db"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.database.models.articles import Articles

# TODO: add logging and remove prints


def insert_in_db(article: Articles, session: Session) -> None:
    """inserts the article object into a db
    :param article: the Articles instance
    :param the sqlalchemy session
    """
    print(f"adding article: {article}...")
    session.add(article)
    try:
        session.commit()
        print(f"Done: added article: {article} !")

    except SQLAlchemyError as e:
        session.rollback()
        raise e
