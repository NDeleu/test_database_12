import click
from models.database_models.database import session
from models.class_models.article import Article
from models.class_models.client import Client
from controllers.auth_controller import login_required_client, login_required
from views.article_view import display_article
from views.menu_view import display_message


@click.group()
def article():
    pass


@login_required_client
def create_article(title, body, client_id):
    try:
        client = session.query(Client).filter_by(id=client_id).first()
        if client:
            article = Article.create(title, body, client)
            display_message(f"Article created: {article}")
        else:
            display_message("Client not found")
    except ValueError as e:
        display_message(str(e))

@login_required
def read_article(article_id):
    article = session.query(Article).filter_by(id=article_id).first()
    if article:
        display_article(article)
    else:
        display_message("Article not found")


@login_required_client
def update_article(article_id, title, body):
    article = session.query(Article).filter_by(id=article_id).first()
    if article:
        kwargs = {'title': title, 'body': body}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if kwargs:
            article.update(**kwargs)
            display_message("Article updated")
        else:
            display_message("No updates provided")
    else:
        display_message("Article not found")


@login_required_client
def delete_article(article_id):
    article = session.query(Article).filter_by(id=article_id).first()
    if article:
        article.delete()
        display_message("Article deleted")
    else:
        display_message("Article not found")


@article.command()
@click.argument('title', type=click.STRING)
@click.argument('body', type=click.STRING)
@click.argument('client_id', type=click.INT)
def create(title, body, client_id):
    create_article(title, body, client_id)


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
