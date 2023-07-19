from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.database_models.database import Base, session
from models.class_models.client import Client
from datetime import datetime


class Article(Base):

    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="articles")

    def __init__(self, title, body, client):
        self.title = title
        self.body = body

        self.client = client

    @classmethod
    def create(cls, title, body, client):
        article = Article(title=title, body=body, client=client)
        session.add(article)
        session.commit()
        return article

    @classmethod
    def read(cls, article_id):
        client = session.query(Client).filter_by(id=article_id).first()
        return client

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.title} écrit le {self.created_date.strftime("%Y-%m-%d %H:%M:%S")}'
