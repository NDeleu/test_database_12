import click
from .administrator_set_controller import create_admin, read_admin, update_admin, delete_admin


@click.group()
def administrator():
    pass


@administrator.command()
def create():
    create_admin()


@administrator.command()
@click.argument('administrator_id', type=int)
def read(administrator_id):
    read_admin(administrator_id)


@administrator.command()
@click.argument('administrator_id', type=int)
@click.option('--surname', default=None)
@click.option('--lastname', default=None)
@click.option('--age', type=int, default=None)
@click.option('--email', default=None)
def update(administrator_id, surname, lastname, age, email):
    update_admin(administrator_id, surname, lastname, age, email)


@administrator.command()
@click.argument('administrator_id', type=int)
def delete(administrator_id):
    delete_admin(administrator_id)
