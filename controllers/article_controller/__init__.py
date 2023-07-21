import click
from .article_set_controller import create_article, read_article, update_article, delete_article


@click.group()
def article():
    pass


@article.command()
def create():
    create_article()


@article.command()
@click.argument('article_id', type=int)
def read(article_id):
    read_article(article_id)


@article.command()
@click.argument('article_id', type=int)
@click.option('--title', default=None)
@click.option('--body', default=None)
def update(article_id, title, body):
    update_article(article_id, title, body)


@article.command()
@click.argument('article_id', type=int)
def delete(article_id):
    delete_article(article_id)