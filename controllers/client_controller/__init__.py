import click
from .client_set_controller import create_client, read_client, update_client, delete_client


@click.group()
def client():
    pass


@client.command()
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