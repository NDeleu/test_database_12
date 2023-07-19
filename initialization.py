import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from sqlalchemy.exc import SQLAlchemyError
import secrets
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.automap import automap_base
from models.database_models.database import Base
from models.class_models.administrator import Administrator
from models.class_models.article import Article
from models.class_models.client import Client
from views.menu_view import display_message
import re


def init_engine_bdd():
    config = ConfigParser()
    config.read('config.ini')

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

    return engine


def try_connect_bdd():
    engine = init_engine_bdd()
    try:
        conn = engine.connect()
        conn.close()
        return True
    except SQLAlchemyError:
        return False


def check_config_ini_exist():
    if os.path.exists('config.ini'):
        return True
    else:
        display_message("The config.ini file does not exist. Please verify the integrity of the repository and retry.")
        return False


def check_alembic_ini_exist():
    if os.path.exists('alembic.ini'):
        return True
    else:
        display_message("The alembic.ini file does not exist. Please verify the integrity of the repository and retry.")
        return False


def sql_init_config():
    while True:
        try:
            database_select_choice = int(input("Select 1 for PostgreSQL or 2 for MySQL: "))
            if database_select_choice == 1:
                database_driver_choice = "postgresql"
                break
            elif database_select_choice == 2:
                database_driver_choice = "mysql"
                break
            else:
                display_message("Invalid choice. Please try again.")
        except ValueError:
            display_message("Invalid input. Please enter a valid choice.")

    while True:
        try:
            username_choice = str(input("Enter your database administrator username: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid username.")

    while True:
        try:
            password_choice = str(input("Enter your database password: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid password.")

    while True:
        try:
            database_name_choice = str(input("Enter your database name: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid database name.")

    return database_driver_choice, username_choice, password_choice, database_name_choice


def set_sql_config_ini():
    config = ConfigParser()
    config.read('config.ini')

    database_driver_choice, username_choice, password_choice, database_name_choice = sql_init_config()

    config.set('sql', 'database_type', database_driver_choice)
    config.set('sql', 'username', username_choice)
    config.set('sql', 'password', password_choice)
    config.set('sql', 'host', 'localhost')
    config.set('sql', 'database_name', database_name_choice)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def check_jwt_secret():
    config = ConfigParser()
    config.read('config.ini')

    jwt_secret = config.get('jwt', 'secret_key_jwt')

    if jwt_secret == "default":
        return False
    else:
        return True


def set_jwt_secret():
    config = ConfigParser()
    config.read('config.ini')

    jwt_secret_key = secrets.token_hex(32)
    config.set('jwt', 'secret_key_jwt', jwt_secret_key)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def url_init_alembic():
    config = ConfigParser()
    config.read('config.ini')

    database_type = config.get('sql', 'database_type')
    username = config.get('sql', 'username')
    password = config.get('sql', 'password')
    host = config.get('sql', 'host')
    database_name = config.get('sql', 'database_name')

    if database_type == "mysql":
        import pymysql
        db_url = f'{database_type}+pymysql://{username}:{password}@{host}:3306/{database_name}'
    else:
        db_url = f'{database_type}://{username}:{password}@{host}:5432/{database_name}'

    return db_url


def set_url_alembic_ini():
    config = ConfigParser()
    config.read('alembic.ini')

    sqlalchemy_url = url_init_alembic()

    config.set('alembic', 'sqlalchemy.url', sqlalchemy_url)

    with open('alembic.ini', 'w') as configfile:
        config.write(configfile)


def check_tables_exist():
    engine = init_engine_bdd()
    conn = engine.connect()

    if not engine.dialect.has_table(conn, 'alembic_version'):
        conn.close()
        return False
    conn.close()
    return True


def check_if_table_empty(table_name):
    engine = init_engine_bdd()
    Session = sessionmaker(bind=engine)
    session = Session()

    Base = automap_base()
    Base.prepare(engine)
    table = Base.classes[table_name]

    count = session.query(table).count()
    session.close()

    if count == 0:
        return True
    else:
        return False


def check_version_file_exist():
    versions_folder_path = 'models/database_models/migrations/versions'
    end_with_file = '_first_commit'

    files = [file for file in os.listdir(versions_folder_path) if file.endswith(end_with_file)]

    if files:
        return True
    else:
        return False

def set_create_administrator():
    while True:
        try:
            surname_choice = str(input("Enter your administrator surname: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid surname.")

    while True:
        try:
            lastname_choice = str(input("Enter your administrator lastname: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid lastname.")

    while True:
        try:
            age_choice = int(input("Enter your administrator age: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid age.")

    while True:
        try:
            email_choice = str(input("Enter your administrator email: "))
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_choice):
                raise ValueError("Email address is not valid")
            break
        except ValueError as e:
            display_message(str(e))

    while True:
        try:
            password_choice = str(input("Enter your administrator password: "))
            break
        except ValueError:
            display_message("Invalid input. Please enter a valid password.")

    return surname_choice, lastname_choice, age_choice, email_choice, password_choice


def create_first_administrator():
    surname, lastname, age, email, password = set_create_administrator()
    administrator = Administrator.create(surname, lastname, age, email, password)
    display_message(f"Administrator created: {administrator}")


def initialization_bdd():
    if try_connect_bdd():
        # Database already connected
        pass
    else:
        if not check_config_ini_exist():
            sys.exit(1)
        else:
            set_sql_config_ini()
            if not try_connect_bdd():
                display_message("Cannot connect to the database, please check if your database is configured and if the informations provided are correct, and retry.")
                sys.exit(1)
            else:
                if not check_jwt_secret():
                    set_jwt_secret()
                if not check_alembic_ini_exist():
                    sys.exit(1)
                else:
                    set_url_alembic_ini()
                if check_version_file_exist():
                    if not check_tables_exist():
                        alembic_cfg = Config('alembic.ini')
                        command.upgrade(alembic_cfg, 'head')
                        if not check_tables_exist():
                            display_message("An error has occurred, please check the status of your database and try again.")
                            sys.exit(1)
                    else:
                        # Database with Alembic already configured
                        pass
                else:
                    alembic_cfg = Config('alembic.ini')
                    command.revision(alembic_cfg, autogenerate=True, message="first commit")
                    if check_version_file_exist():
                        if not check_tables_exist():
                            alembic_cfg = Config('alembic.ini')
                            command.upgrade(alembic_cfg, 'head')
                            if not check_tables_exist():
                                display_message("An error has occurred, please check the status of your database and try again")
                    else:
                        display_message("The migration file could not be created. Please verify the integrity of the repository and retry.")
                        sys.exit(1)
                if check_if_table_empty("administrators"):
                    create_first_administrator()
                else:
                    # An administrator already exists
                    pass
    display_message("Initialization already configured.")


if __name__ == "__main__":
    initialization_bdd()
