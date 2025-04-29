"""orm model"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    """we omit filename, useless."""

    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Article(title='{self.title}', category='{self.category}', content='{self.content}')"
