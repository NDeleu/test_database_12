import click
from .auth_controller import login, logout
from .administrator_controller import administrator
from .client_controller import client
from .article_controller import article
from controllers.link_bdd.first_initialization_bdd import first_init_bdd
from controllers.link_bdd.check_first_avenger import check_administrator_existence
from controllers.link_bdd.create_first_avenger import create_first_administrator


@click.group()
def cli():
    pass


cli.add_command(administrator, name='administrator')
cli.add_command(article, name='article')
cli.add_command(client, name='client')
cli.add_command(login, name='login')
cli.add_command(logout, name='logout')