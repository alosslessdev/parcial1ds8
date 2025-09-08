from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.prompt import Confirm
from datetime import datetime

from estado import EstadoParqueo
from Eventos import HistorialEventos

import os

console = Console()

# Inicialización de objetos globales
CAPACIDAD_MAX = 10
parqueo = EstadoParqueo(capacidad_max=CAPACIDAD_MAX)
historial = HistorialEventos()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    console.print(Panel("[bold cyan]SISTEMA DE PARQUEO[/bold cyan]", expand=False))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Opción", justify="center", style="bold yellow")
    table.add_column("Descripción", style="green")
    table.add_row("1", "Simular entrada de auto")
    table.add_row("2", "Simular salida de auto")
    table.add_row("3", "Ver estado del parqueo")
    table.add_row("4", "Ver historial de eventos")
    table.add_row("5", "Salir")
    console.print(table)

def simular_entrada():
    console.print(Panel("[bold green]Simulación de entrada[/bold green]", expand=False))
    placa = Prompt.ask("Ingrese la placa del auto").strip().upper()
    if not placa:
        console.print("[red]Placa no válida[/red]")
        return
    if not parqueo.puede_admitir():
        console.print("[red]¡Parqueo lleno! No se puede admitir otro auto.[/red]")
        return
    parqueo.actualizar(parqueo.ocupados + 1)
    hora = datetime.now()
    historial.guardar_evento(placa, hora, "entrada")
    console.print(f"[green]Auto {placa} ha entrado. Hora: {hora.strftime('%Y-%m-%d %H:%M:%S')}[/green]")

def simular_salida():
    console.print(Panel("[bold green]Simulación de salida[/bold green]", expand=False))
    placa = Prompt.ask("Ingrese la placa del auto").strip().upper()
    if not placa:
        console.print("[red]Placa no válida[/red]")
        return
    if parqueo.ocupados == 0:
        console.print("[red]No hay autos para salir.[/red]")
        return
    # Para demo: tarifa fija (puedes cambiar por cálculo real)
    tarifa = 2.5
    parqueo.actualizar(parqueo.ocupados - 1)
    hora = datetime.now()
    historial.guardar_evento(placa, hora, "salida", tarifa)
    console.print(f"[yellow]Auto {placa} ha salido. Hora: {hora.strftime('%Y-%m-%d %H:%M:%S')} | Tarifa: ${tarifa}[/yellow]")

def ver_estado():
    estado = parqueo.resumen()
    panel_text = (
        f"[bold]Capacidad:[/bold] {estado['capacidad']}\n"
        f"[bold]Ocupados:[/bold] {estado['ocupados']}\n"
        f"[bold]Libres:[/bold] {estado['libres']}\n"
        f"[bold]Porcentaje:[/bold] {estado['porcentaje']}%\n"
        f"[bold]Nivel:[/bold] {estado['nivel']}\n"
        f"[bold]Pueden entrar:[/bold] {estado['pueden_entrar']}\n"
        f"{parqueo.gauge_ascii(30)}"
    )
    console.print(Panel(panel_text, title="Estado Actual del Parqueo", expand=False))

def ver_historial():
    table = Table(title="Historial de eventos", show_lines=True)
    table.add_column("Placa", style="cyan", justify="center")
    table.add_column("Fecha y Hora", style="green")
    table.add_column("Tipo", style="magenta")
    table.add_column("Tarifa", style="yellow", justify="right")

    if Confirm.ask("¿Desea ver el historial de una placa específica?", default=False):
        placa = Prompt.ask("Ingrese la placa").strip().upper()
        eventos = historial.obtener_historial(placa)
        if not eventos:
            console.print(f"[red]No hay eventos registrados para la placa {placa}[/red]")
            return
        for placa_ev, hora, tipo, tarifa in eventos:
            table.add_row(placa_ev, hora.strftime("%Y-%m-%d %H:%M:%S"), tipo, f"${tarifa:.2f}" if tipo == "salida" else "-")
    else:
        todos = historial.obtener_todos()
        for placa_ev, lista in todos.items():
            for ev in lista:
                placa_ev, hora, tipo, tarifa = ev
                table.add_row(placa_ev, hora.strftime("%Y-%m-%d %H:%M:%S"), tipo, f"${tarifa:.2f}" if tipo == "salida" else "-")
    console.print(table)

def main():
    while True:
        mostrar_menu()
        opcion = Prompt.ask("[bold white]Seleccione una opción[/bold white]", choices=["1", "2", "3", "4", "5"])
        if opcion == "1":
            simular_entrada()
            console.input("[cyan]Presione Enter para continuar...[/cyan]")
        elif opcion == "2":
            simular_salida()
            console.input("[cyan]Presione Enter para continuar...[/cyan]")
        elif opcion == "3":
            ver_estado()
            console.input("[cyan]Presione Enter para continuar...[/cyan]")
        elif opcion == "4":
            ver_historial()
            console.input("[cyan]Presione Enter para continuar...[/cyan]")
        elif opcion == "5":
            console.print(Panel("[bold green]¡Hasta luego![/bold green]", expand=False))
            break

if __name__ == "__main__":
    main()