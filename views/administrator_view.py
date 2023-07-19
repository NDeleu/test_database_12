from rich.console import Console

console = Console()


def display_administrator(administrator):
    console.print("[bold green]Administrator found:[/bold green]")
    console.print(f"ID: {administrator.id}")
    console.print(f"Surname: {administrator.surname}")
    console.print(f"Lastname: {administrator.lastname}")
    console.print(f"Age: {administrator.age}")
    console.print(f"Email: {administrator.email}")
