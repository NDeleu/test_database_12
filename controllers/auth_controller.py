import os
import click
from models.database_models.database import session
from models.class_models.administrator import Administrator
from models.class_models.client import Client
from datetime import datetime, timedelta
import jwt
from configparser import ConfigParser
from views.menu_view import display_message


script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
config_file = os.path.join(root_dir, 'config.ini')

config = ConfigParser()
config.read(config_file)

SECRET_KEY = config.get('jwt', 'secret_key_jwt')


@click.command()
def login():
    email = click.prompt("Email", type=click.STRING)
    password = click.prompt("Password", type=click.STRING, hide_input=True)

    administrator = session.query(Administrator).filter_by(email=email).first()
    client = session.query(Client).filter_by(email=email).first()

    if administrator:
        if administrator.verify_password(password):
            token = generate_token(administrator.id, "administrator")
            administrator.token = token
            administrator.token_expiration = datetime.utcnow() + timedelta(minutes=10)
            session.commit()
            save_token_to_file(token)
            display_message("Administrator logged in successfully")
        else:
            display_message("Incorrect password for administrator")
    elif client:
        if client.verify_password(password):
            token = generate_token(client.id, "client")
            client.token = token
            client.token_expiration = datetime.utcnow() + timedelta(minutes=10)
            session.commit()
            save_token_to_file(token)
            display_message("Client logged in successfully")
        else:
            display_message("Incorrect password for client")
    else:
        display_message("User not found")


def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=7)  # Exemple : le token expire dans 7 jours
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def save_token_to_file(token):
    with open("token.txt", "w") as file:
        file.write(token)


def clear_token_from_file():
    with open("token.txt", "w") as file:
        file.write("")


def get_logged_in_administrator():
    token = get_token_from_file()
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return session.query(Administrator).filter_by(id=user_id).first()
        except jwt.ExpiredSignatureError:
            clear_token_from_file()
            return None
    return None


def get_logged_in_client():
    token = get_token_from_file()
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return session.query(Client).filter_by(id=user_id).first()
        except jwt.ExpiredSignatureError:
            clear_token_from_file()
            return None
    return None


def get_logged_in_user():
    token = get_token_from_file()
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            administrator = session.query(Administrator).filter_by(id=user_id).first()
            client = session.query(Client).filter_by(id=user_id).first()
            if administrator:
                return administrator
            elif client:
                return client
            else:
                clear_token_from_file()
                return None
        except jwt.ExpiredSignatureError:
            clear_token_from_file()
            return None
    return None


def get_token_from_file():
    try:
        with open("token.txt", "r") as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        return None


def login_required_admin(func):
    def wrapper(*args, **kwargs):
        administrator = get_logged_in_administrator()
        if administrator:
            return func(*args, **kwargs)
        else:
            display_message("Permission denied. Please log in as an administrator.")
    return wrapper


def login_required_client(func):
    def wrapper(*args, **kwargs):
        client = get_logged_in_client()
        if client:
            return func(*args, **kwargs)
        else:
            display_message("Permission denied. Please log in as a client.")
    return wrapper


def login_required(func):
    def wrapper(*args, **kwargs):
        user = get_logged_in_user()
        if user:
            return func(*args, **kwargs)
        else:
            display_message("Permission denied. Please log in.")
    return wrapper


@click.command()
def logout():
    user = get_logged_in_user()

    if isinstance(user, Administrator):
        user.token = None
        user.token_expiration = None
        session.commit()
        clear_token_from_file()
        display_message("Administrator logged out successfully")
    elif isinstance(user, Client):
        user.token = None
        user.token_expiration = None
        session.commit()
        clear_token_from_file()
        display_message("Client logged out successfully")
    else:
        display_message("No user logged in")
