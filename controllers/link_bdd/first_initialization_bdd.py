import os
import secrets
import sys

from sqlalchemy.exc import SQLAlchemyError
from models import engine
from views.menu_view import display_message
from configparser import ConfigParser
import re


def info_init_bdd():
    while True:
        display_message("An error occurred during execution. Your database may not be initialized yet, do you want to initialize it now?")
        try:
            init_select_choice = int(input(display_message("Select 1 for Yes or 2 for No: ")))
            if init_select_choice == 1:
                init_bdd_choice = True
                break
            elif init_select_choice == 2:
                init_bdd_choice = False
                break
            else:
                display_message("Invalid choice. Please try again.")
        except ValueError:
            display_message("Invalid input. Please enter a valid choice.")


def sql_init_config():
    while True:
        try:
            database_select_choice = int(input(display_message("Select 1 for PostgreSQL or 2 for MySQL: ")))
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
        username_choice = str(input(
            display_message("Enter your database administrator username: ")))

        if re.match("^[a-zA-Z0-9]+$", username_choice):
            break
        else:
            display_message(
                "Invalid input. Please enter a valid username without special characters or spaces.")

    while True:
        password_choice = str(
            input(display_message("Enter your database password: ")))

        if re.match("^[a-zA-Z0-9]+$", password_choice):
            break
        else:
            display_message(
                "Invalid input. Please enter a valid password without special characters or spaces.")

    while True:
        database_name_choice = str(
            input(display_message("Enter your database name: ")))

        # Vérification avec une expression régulière pour restreindre à alphanumérique
        if re.match("^[a-zA-Z0-9]+$", database_name_choice):
            break
        else:
            display_message(
                "Invalid input. Please enter a valid database name without special characters or spaces.")

    sett = {
        'database_type': database_driver_choice,
        'username': username_choice,
        'password': password_choice,
        'database_name': database_name_choice,
    }

    return sett


def set_sql_config_ini(sql_init_config_set):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    controllers_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(controllers_dir)
    config_file = os.path.join(root_dir, 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    config.set('sql', 'database_type', sql_init_config_set['database_type'])
    config.set('sql', 'username', sql_init_config_set['username'])
    config.set('sql', 'password', sql_init_config_set['password'])
    config.set('sql', 'host', 'localhost')
    config.set('sql', 'database_name', sql_init_config_set['database_name'])

    with open(config_file, 'w') as confchange:
        config.write(confchange)


def check_config_ini_exist():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    controllers_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(controllers_dir)
    config_file = os.path.join(root_dir, 'config.ini')
    if os.path.exists(config_file):
        return True
    else:
        display_message("The config.ini file does not exist. Please verify the integrity of the repository and retry.")
        return False


def try_connect_bdd(engine):
    try:
        conn = engine.connect()
        conn.close()
        return True
    except SQLAlchemyError:
        return False


def check_default_jwt_secret():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    controllers_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(controllers_dir)
    config_file = os.path.join(root_dir, 'config.ini')
    config = ConfigParser()
    config.read(config_file)

    jwt_secret = config.get('jwt', 'secret_key_jwt')

    if jwt_secret == "default":
        return True
    else:
        return False


def set_jwt_secret():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    controllers_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(controllers_dir)
    config_file = os.path.join(root_dir, 'config.ini')
    config = ConfigParser()
    config.read(config_file)

    jwt_secret_key = secrets.token_hex(32)
    config.set('jwt', 'secret_key_jwt', jwt_secret_key)

    with open(config_file, 'w') as confchange:
        config.write(confchange)


def first_init_bdd():
    if info_init_bdd():
        if try_connect_bdd(engine):
            if check_default_jwt_secret():
                set_jwt_secret()
            else:
                pass
        else:
            if check_config_ini_exist():
                set_sql_config_ini(sql_init_config())
                if try_connect_bdd(engine):
                    if check_default_jwt_secret():
                        set_jwt_secret()
                    else:
                        if try_connect_bdd(engine):
                            pass
                        else:
                            display_message("The database could not be initialized correctly, please try again later. If the problem persists, please contact technical support.")
                            sys.exit(1)
                else:
                    display_message("The database could not be initialized correctly, please try again later. If the problem persists, please contact technical support.")
                    sys.exit(1)
            else:
                display_message("Try to fix the runtime problem and try again")
                sys.exit(1)
    else:
        display_message("Try to fix the runtime problem and try again")
        sys.exit(1)
    display_message("Your database is configured and ready to use")
