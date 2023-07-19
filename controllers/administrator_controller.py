import click
import re
from models.database_models.database import session
from models.class_models.administrator import Administrator
from controllers.auth_controller import login_required_admin
from views.administrator_view import display_administrator
from views.menu_view import display_message


@click.group()
def administrator():
    pass


@login_required_admin
def create_admin(surname, lastname, age, email, password):
    try:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email address is not valid")

        administrator = Administrator.create(surname, lastname, age, email,
                                             password)
        display_message(f"Administrator created: {administrator}")
    except ValueError as e:
        display_message(str(e))


@login_required_admin
def read_admin(administrator_id):
    administrator = session.query(Administrator).filter_by(id=administrator_id).first()
    if administrator:
        display_administrator(administrator)
    else:
        display_message("Administrator not found")


@login_required_admin
def update_admin(administrator_id, surname, lastname, age, email):
    administrator = session.query(Administrator).filter_by(id=administrator_id).first()
    if administrator:
        kwargs = {'surname': surname, 'lastname': lastname, 'age': age, 'email': email}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if kwargs:
            administrator.update(**kwargs)
            display_message("Administrator updated")
        else:
            display_message("No updates provided")
    else:
        display_message("Administrator not found")


@login_required_admin
def delete_admin(administrator_id):
    administrator = session.query(Administrator).filter_by(id=administrator_id).first()
    if administrator:
        administrator.delete()
        display_message("Administrator deleted")
    else:
        display_message("Administrator not found")


@administrator.command()
@click.argument('surname', type=click.STRING)
@click.argument('lastname', type=click.STRING)
@click.argument('age', type=click.INT)
@click.argument('email', type=click.STRING)
@click.argument('password', type=click.STRING)
def create(surname, lastname, age, email, password):
    create_admin(surname, lastname, age, email, password)


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