import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser
from sqlalchemy_utils import database_exists, create_database

def initialize_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(models_dir)
    config_file = os.path.join(root_dir, 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    database_type = config.get('sql', 'database_type')
    username = config.get('sql', 'username')
    password = config.get('sql', 'password')
    host = config.get('sql', 'host')
    database_name = config.get('sql', 'database_name')

    if database_type == "mysql":
        import pymysql
        db_url = f'{database_type}+pymysql://{username}:{password}@{host}:3306/{database_name}'
        engine = create_engine(db_url, encoding='utf8')
    elif database_type == "postgresql":
        db_url = f'{database_type}://{username}:{password}@{host}:5432/{database_name}'
        engine = create_engine(db_url)
    else:
        engine = None

    Base = declarative_base()

    Session = sessionmaker(bind=engine)
    session = Session()

    # Autres opérations de configuration ou d'initialisation de la base de données

    return engine, Base, session

# Exemple d'utilisation de la fonction initialize_database()
engine, Base, session = initialize_database()