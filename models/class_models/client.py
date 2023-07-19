from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import text
from models.database_models.database import Base, session
from passlib.hash import bcrypt


class Client(Base):

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    email = Column(String)
    password = Column(String)
    token = Column(String)
    token_expiration = Column(DateTime)
    administrator_id = Column(Integer, ForeignKey('administrators.id'))
    administrator = relationship("Administrator", back_populates="clients")
    articles = relationship("Article", back_populates="client", cascade="all, delete")

    def __init__(self, surname, lastname, age, email, administrator, password):
        self.surname = surname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.password = bcrypt.hash(password)
        self.administrator = administrator

    @classmethod
    def create(cls, surname, lastname, age, email, administrator, password):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM administrators WHERE email=:email) "
                "OR EXISTS (SELECT 1 FROM clients WHERE email=:email)"),
            {"email": email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "L'adresse e-mail existe déjà pour un administrateur ou un client.")

        client = Client(surname=surname, lastname=lastname, age=age,
                        email=email, administrator=administrator,
                        password=password)
        session.add(client)
        session.commit()
        return client

    @classmethod
    def read(cls, client_id):
        client = session.query(Client).filter_by(id=client_id).first()
        return client

    def set_email(self, new_email):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM administrators WHERE email=:new_email) "
                "OR EXISTS (SELECT 1 FROM clients WHERE email=:new_email)"),
            {"new_email": new_email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "L'adresse e-mail existe déjà pour un administrateur ou un client.")

        self.email = new_email

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'email':
                self.set_email(value)
            else:
                setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def __str__(self):
        return f'{self.surname} {self.lastname} qui a {self.age} ans'
