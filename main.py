from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import os

console = Console()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    console.print(Panel("[bold cyan]SISTEMA DE PARQUEO[/bold cyan]", expand=False))

    table = Table(show_header=True, header_style="bold magenta", expand=False)
    table.add_column("Opción", justify="center", style="bold yellow")
    table.add_column("Descripción", style="green")
    table.add_row("1", "Simular entrada de autos")
    table.add_row("2", "Simular salida de autos")
    table.add_row("3", "Ver estado del parqueo")
    table.add_row("4", "Ver historial de eventos")
    table.add_row("5", "Salir")
    console.print(table)

def main():
    while True:
        mostrar_menu()
        opcion = Prompt.ask("[bold white]Seleccione una opción[/bold white]", choices=["1", "2", "3", "4", "5"])
        if opcion == "1":
            console.print("[green]Función de entrada de autos (a implementar)[/green]")
            console.input("[bold cyan]Presione Enter para continuar...[/bold cyan]")
        elif opcion == "2":
            console.print("[green]Función de salida de autos (a implementar)[/green]")
            console.input("[bold cyan]Presione Enter para continuar...[/bold cyan]")
        elif opcion == "3":
            console.print("[yellow]Función de estado del parqueo (a implementar)[/yellow]")
            console.input("[bold cyan]Presione Enter para continuar...[/bold cyan]")
        elif opcion == "4":
            console.print("[yellow]Función de historial de eventos (a implementar)[/yellow]")
            console.input("[bold cyan]Presione Enter para continuar...[/bold cyan]")
        elif opcion == "5":
            console.print(Panel("[bold green]¡Hasta luego![/bold green]", expand=False))
            break

if __name__ == "__main__":
    main()   