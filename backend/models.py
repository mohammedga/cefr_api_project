# backend/models.py
from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    level = Column(String(10), nullable=True)
    minutes = Column(Integer, default=3)
    text = Column(JSON, nullable=False)   # English paragraphs (list)
    ar = Column(JSON, nullable=True)      # Arabic paragraphs (list)
    vocab = Column(JSON, nullable=True)   # list of [en, ar]
    quiz = Column(JSON, nullable=True)    # list of {q, options, answer}
