import click
from controllers.administrator_controller import administrator
from controllers.article_controller import article
from controllers.client_controller import client
from controllers.auth_controller import login, logout


@click.group()
def cli():
    pass


cli.add_command(administrator, name='administrator')
cli.add_command(article, name='article')
cli.add_command(client, name='client')
cli.add_command(login, name='login')
cli.add_command(logout, name='logout')

if __name__ == '__main__':
    cli()
