from rich.console import Console

console = Console()


def display_message(message):
    console.print(f"[green red]{message}[/green red]")
