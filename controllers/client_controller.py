import click
import re
from models.database_models.database import session
from models.class_models.client import Client
from models.class_models.administrator import Administrator
from controllers.auth_controller import login_required_admin
from views.client_view import display_client
from views.menu_view import display_message


@click.group()
def client():
    pass


@login_required_admin
def create_client(surname, lastname, age, email, administrator_id, password):
    try:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email address is not valid")

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


@client.command()
@click.argument('surname', type=click.STRING)
@click.argument('lastname', type=click.STRING)
@click.argument('age', type=click.INT)
@click.argument('email', type=click.STRING)
@click.argument('administrator_id', type=click.INT)
@click.argument('password', type=click.STRING)
def create(surname, lastname, age, email, administrator_id, password):
    create_client(surname, lastname, age, email, administrator_id, password)


@client.command()
@click.argument('client_id', type=int)
def read(client_id):
    read_client(client_id)


@client.command()
@click.argument('client_id', type=int)
@click.option('--surname', default=None)
@click.option('--lastname', default=None)
@click.option('--age', type=int, default=None)
@click.option('--email', default=None)
def update(client_id, surname, lastname, age, email):
    update_client(client_id, surname, lastname, age, email)


@client.command()
@click.argument('client_id', type=int)
def delete(client_id):
    delete_client(client_id)
