import click
from .auth_set_controller import login_set, logout_set


@click.command()
def login():
    login_set()


@click.command()
def logout():
    logout_set()
