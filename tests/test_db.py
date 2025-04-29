"""Test database connection and model with PostgreSQL"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.backend.database.db import CONN_STR
from src.backend.database.models.article import Article


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


def test_article_model():
    """Test Article model creation"""
    article = Article(category="tech", title="Test Title", content="Test Content")

    assert article.category == "tech"  # pyright: ignore
    assert article.title == "Test Title"  # pyright: ignore
    assert article.content == "Test Content"  # pyright: ignore


def test_db_session(test_postgres_db):
    """Test database session works with PostgreSQL"""
    article = Article(
        category="politics", title="News Article", content="Political content"
    )

    test_postgres_db.add(article)
    test_postgres_db.commit()

    result = test_postgres_db.query(Article).filter_by(title="News Article").first()

    assert result is not None
    assert result.category == "politics"
    assert result.content == "Political content"


def test_db_query(test_postgres_db):
    """Test PostgreSQL database queries"""
    articles = [
        Article(category="tech", title="Tech News", content="Technology content"),
        Article(category="sports", title="Sports Update", content="Sports content"),
        Article(category="tech", title="More Tech", content="More technology"),
    ]

    for article in articles:
        test_postgres_db.add(article)
    test_postgres_db.commit()

    tech_articles = test_postgres_db.query(Article).filter_by(category="tech").all()
    assert len(tech_articles) == 2

    sports_article = (
        test_postgres_db.query(Article).filter_by(title="Sports Update").first()
    )
    assert sports_article.category == "sports"
