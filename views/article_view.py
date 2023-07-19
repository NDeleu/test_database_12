from rich.console import Console

console = Console()


def display_article(article):
    console.print("[bold green]Article found:[/bold green]")
    console.print(f"ID: {article.id}")
    console.print(f"Title: {article.title}")
    console.print(f"Body: {article.body}")
    console.print(f"Created Date: {article.created_date}")
