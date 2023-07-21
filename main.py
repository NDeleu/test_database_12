import click
from controllers.administrator_controller import administrator
from controllers.article_controller import article
from controllers.client_controller import client
from controllers.auth_controller import login, logout
from controllers.link_bdd.first_initialization_bdd import first_init_bdd
from controllers.link_bdd.check_first_avenger import check_administrator_existence
from controllers.link_bdd.create_first_avenger import create_first_administrator
from sqlalchemy.exc import SQLAlchemyError


@click.group()
def cli():
    pass


cli.add_command(administrator, name='administrator')
cli.add_command(article, name='article')
cli.add_command(client, name='client')
cli.add_command(login, name='login')
cli.add_command(logout, name='logout')

if __name__ == '__main__':
    try:
        if check_administrator_existence():
            cli()
        else:
            create_first_administrator()
    except SQLAlchemyError:
        first_init_bdd()
