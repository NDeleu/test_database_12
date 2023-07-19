from rich.console import Console

console = Console()


def display_message(message):
    console.print(f"[bold red]{message}[/bold red]")
