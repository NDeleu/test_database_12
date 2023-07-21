import click
import re
from models.database_models.database import session
from models.class_models.article import Article
from models.class_models.client import Client
from controllers.auth_controller.auth_set_controller import login_required_client, login_required
from views.article_view import display_article
from views.menu_view import display_message


@login_required_client
def create_article():
    while True:
        title = click.prompt("Title", type=click.STRING)

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', title):
            display_message("The title should not contain special characters. Try again")
        else:
            break

    while True:
        body = click.prompt("Body", type=click.STRING)

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', body):
            display_message("The body should not contain special characters. Try again")
        else:
            break

    while True:
        try:
            client_id = click.prompt("ID Client", type=click.INT)
            break
        except click.BadParameter:
            display_message("Invalid input. Please enter a valid ID.")

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
