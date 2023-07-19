from rich.console import Console

console = Console()


def display_client(client):
    console.print("[bold green]Client found:[/bold green]")
    console.print(f"ID: {client.id}")
    console.print(f"Surname: {client.surname}")
    console.print(f"Lastname: {client.lastname}")
    console.print(f"Age: {client.age}")
    console.print(f"Email: {client.email}")
