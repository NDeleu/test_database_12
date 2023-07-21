import re
import click
from models.database_models.database import session
from models.class_models.administrator import Administrator
from controllers.auth_controller.auth_set_controller import login_required_admin
from views.administrator_view import display_administrator
from views.menu_view import display_message


def create_admin():
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
        password = click.prompt("Password", type=click.STRING, hide_input=True)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            display_message("Password should not contain special characters. Try again.")
        elif len(password) < 6:
            display_message("Password should be at least 6 characters long. Try again.")
        else:
            break

    try:
        administrator = Administrator.create(surname, lastname, age, email, password)
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
