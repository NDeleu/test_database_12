from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import text
from passlib.hash import bcrypt
from models.database_models.database import Base, session


class Administrator(Base):

    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    email = Column(String)
    password = Column(String)
    token = Column(String)
    token_expiration = Column(DateTime)
    clients = relationship("Client", back_populates="administrator", cascade="all, delete")

    def __init__(self, surname, lastname, age, email, password):
        self.surname = surname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.password = bcrypt.hash(password)

    @classmethod
    def create(cls, surname, lastname, age, email, password):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM administrators WHERE email=:email) "
                "OR EXISTS (SELECT 1 FROM clients WHERE email=:email)"),
            {"email": email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "L'adresse e-mail existe déjà pour un administrateur ou un client.")

        administrator = Administrator(surname=surname, lastname=lastname,
                                      age=age, email=email, password=password)
        session.add(administrator)
        session.commit()
        return administrator

    @classmethod
    def read(cls, administrator_id):
        administrator = session.query(Administrator).filter_by(id=administrator_id).first()
        return administrator

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
