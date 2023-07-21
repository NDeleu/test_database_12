import re
import click
from models.database_models.database import session
from models.class_models.client import Client
from models.class_models.administrator import Administrator
from controllers.auth_controller.auth_set_controller import login_required_admin
from views.client_view import display_client
from views.menu_view import display_message


@login_required_admin
def create_client():
    while True:
        surname = click.prompt("Surname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', surname):
            display_message("Surname should not contain special characters. Try again.")
        else:
            break

    while True:
        lastname = click.prompt("Lastname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', lastname):
            display_message("Lastname should not contain special characters. Try again.")
        else:
            break

    while True:
        try:
            age = click.prompt("Age", type=click.INT)
            break
        except click.BadParameter:
            display_message("Invalid input. Please enter a valid age.")

    while True:
        email = click.prompt("Email", type=click.STRING)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Email address is not valid. Please try again.")
        else:
            break

    while True:
        try:
            administrator_id = click.prompt("ID Administrator", type=click.INT)
            break
        except click.BadParameter:
            display_message("Invalid input. Please enter a valid ID.")

    while True:
        password = click.prompt("Password", type=click.STRING, hide_input=True)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            display_message(
                "Password should not contain special characters. Try again.")
        elif len(password) < 6:
            display_message(
                "Password should be at least 6 characters long. Try again.")
        else:
            break
    try:
        administrator = session.query(Administrator).filter_by(id=administrator_id).first()
        if administrator:
            client = Client.create(surname, lastname, age, email, administrator, password)
            display_message(f"Client created: {client}")
        else:
            display_message("Administrator not found")
    except ValueError as e:
        display_message(str(e))


@login_required_admin
def read_client(client_id):
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        display_client(client)
    else:
        display_message("Client not found")


@login_required_admin
def update_client(client_id, surname, lastname, age, email):
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        kwargs = {'surname': surname, 'lastname': lastname, 'age': age, 'email': email}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if kwargs:
            client.update(**kwargs)
            display_message("Client updated")
        else:
            display_message("No updates provided")
    else:
        display_message("Client not found")


@login_required_admin
def delete_client(client_id):
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        client.delete()
        display_message("Client deleted")
    else:
        display_message("Client not found")
