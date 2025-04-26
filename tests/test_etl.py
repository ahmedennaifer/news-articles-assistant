"""Test ETL functionality with PostgreSQL database"""

import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.api.database.db import CONN_STR
from src.api.database.models.article import Article
from src.api.etl.helpers.convert_to_article import convert_to_article
from src.api.etl.helpers.insert_in_db import insert_in_db


@pytest.fixture
def test_postgres_db():
    """Connect to test PostgreSQL database"""
    test_conn_str = CONN_STR

    engine = create_engine(test_conn_str)

    session = Session(engine)

    session.execute(text("DELETE FROM articles"))
    session.commit()

    yield session

    session.execute(text("DELETE FROM articles"))
    session.commit()
    session.close()


def test_convert_to_article():
    """Test converting pandas Series to Article object"""
    test_row = pd.Series(
        {"category": "tech", "title": "Test Article", "content": "This is test content"}
    )

    article = convert_to_article(test_row)

    assert isinstance(article, Article)
    assert article.category == "tech"  # pyright: ignore
    assert article.title == "Test Article"  # pyright: ignore
    assert article.content == "This is test content"  # pyright: ignore


def test_insert_in_db(test_postgres_db):
    """Test inserting an article into PostgreSQL database"""
    article = Article(
        category="business", title="Business News", content="Economic content"
    )

    import builtins

    original_print = builtins.print
    builtins.print = lambda *args, **kwargs: None
    try:
        insert_in_db(article, test_postgres_db)
    finally:
        builtins.print = original_print

    result = test_postgres_db.query(Article).filter_by(title="Business News").first()

    assert result is not None
    assert result.category == "business"
    assert result.content == "Economic content"


def test_etl_workflow(test_postgres_db):
    """Test the complete ETL workflow with PostgreSQL: convert then insert"""
    test_data = pd.DataFrame(
        {
            "category": ["science", "health"],
            "title": ["Science News", "Health Tips"],
            "content": ["Scientific discovery", "Stay healthy"],
        }
    )

    import builtins

    original_print = builtins.print
    builtins.print = lambda *args, **kwargs: None

    try:
        for _, row in test_data.iterrows():
            article = convert_to_article(row)

            insert_in_db(article, test_postgres_db)
    finally:
        builtins.print = original_print

    results = test_postgres_db.query(Article).all()

    assert len(results) == 2

    titles = sorted([article.title for article in results])
    assert titles == ["Health Tips", "Science News"]

