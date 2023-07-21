from .class_models.administrator import Administrator
from .class_models.client import Client
from .class_models.article import Article

from .database_models.database import Base, engine, session


Base.metadata.create_all(engine)
