import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser


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
else:
    db_url = f'{database_type}://{username}:{password}@{host}:5432/{database_name}'
    engine = create_engine(db_url)

try:
    conn = engine.connect()
    conn.close()
except Exception as e:
    print("Erreur lors de la connexion à la base de données:", e)
    sys.exit(1)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
