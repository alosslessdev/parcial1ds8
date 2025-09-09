from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.prompt import Confirm, IntPrompt
from datetime import datetime
import random

from estado import EstadoParqueo
from Eventos import HistorialEventos
from autos import Autos

import os

console = Console()

# Inicialización de objetos globales
CAPACIDAD_MAX = 10
TARIFA_POR_HORA = 2.5
parqueo = EstadoParqueo(capacidad_max=CAPACIDAD_MAX)
historial = HistorialEventos()
# Lista para mantener las placas de autos actualmente estacionados
autos_estacionados = []

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    console.print(Panel("[bold cyan]SISTEMA DE PARQUEO INTELIGENTE[/bold cyan]", expand=False))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Opción", justify="center", style="bold yellow")
    table.add_column("Descripción", style="green")
    table.add_row("1", "Simular entrada de auto (individual)")
    table.add_row("2", "Simular salida de auto (individual)")
    table.add_row("3", "Simulación por ciclos (múltiples autos)")
    table.add_row("4", "Ver estado del parqueo")
    table.add_row("5", "Ver autos actualmente estacionados")
    table.add_row("6", "Ver historial de eventos")
    table.add_row("7", "Simulación automática aleatoria")
    table.add_row("8", "Salir")
    console.print(table)

def generar_tarifa_aleatoria():
    """Genera una tarifa aleatoria basada en tiempo simulado"""
    horas_simuladas = random.uniform(0.5, 8.0)  # Entre 30 min y 8 horas
    return round(horas_simuladas * TARIFA_POR_HORA, 2)

def simular_entrada():
    console.print(Panel("[bold green]Simulación de entrada[/bold green]", expand=False))
    
    if not parqueo.puede_admitir():
        console.print("[red]¡Parqueo lleno! No se puede admitir otro auto.[/red]")
        return
    
    # Opción de generar placa automáticamente o ingresarla manualmente
    auto_generar = Confirm.ask("¿Desea generar una placa automáticamente?", default=True)
    
    if auto_generar:
        auto = Autos()
        placa = auto.get_placa()
        console.print(f"[blue]Placa generada automáticamente: {placa}[/blue]")
    else:
        placa = Prompt.ask("Ingrese la placa del auto").strip().upper()
        if not placa:
            console.print("[red]Placa no válida[/red]")
            return
    
    # Verificar si el auto ya está estacionado
    if placa in autos_estacionados:
        console.print(f"[red]El auto {placa} ya está estacionado en el parqueo.[/red]")
        return
    
    # Actualizar estado del parqueo
    parqueo.actualizar(parqueo.ocupados + 1)
    autos_estacionados.append(placa)
    
    hora = datetime.now()
    historial.guardar_evento(placa, hora, "entrada")
    
    console.print(f"[green]Auto {placa} ha entrado. Hora: {hora.strftime('%Y-%m-%d %H:%M:%S')}[/green]")
    mostrar_estado_resumido()

def simular_salida():
    console.print(Panel("[bold green]Simulación de salida[/bold green]", expand=False))
    
    if parqueo.ocupados == 0:
        console.print("[red]No hay autos para salir.[/red]")
        return
    
    # Mostrar autos disponibles para salir
    if autos_estacionados:
        console.print("[cyan]Autos actualmente estacionados:[/cyan]")
        for i, placa in enumerate(autos_estacionados, 1):
            console.print(f"  {i}. {placa}")
    
    placa = Prompt.ask("Ingrese la placa del auto que va a salir").strip().upper()
    if not placa:
        console.print("[red]Placa no válida[/red]")
        return
    
    if placa not in autos_estacionados:
        console.print(f"[red]El auto {placa} no está actualmente en el parqueo.[/red]")
        return
    
    # Calcular tarifa (simulada)
    tarifa = generar_tarifa_aleatoria()
    
    # Actualizar estado
    parqueo.actualizar(parqueo.ocupados - 1)
    autos_estacionados.remove(placa)
    
    hora = datetime.now()
    historial.guardar_evento(placa, hora, "salida", tarifa)
    
    console.print(f"[yellow]Auto {placa} ha salido. Hora: {hora.strftime('%Y-%m-%d %H:%M:%S')} | Tarifa: ${tarifa}[/yellow]")
    mostrar_estado_resumido()

def simulacion_por_ciclos():
    """Permite simular múltiples entradas y salidas en un ciclo"""
    console.print(Panel("[bold blue]Simulación por Ciclos[/bold blue]", expand=False))
    
    try:
        entradas = IntPrompt.ask("¿Cuántos autos quieren entrar?", default=0)
        salidas = IntPrompt.ask("¿Cuántos autos quieren salir?", default=0)
        
        if entradas < 0 or salidas < 0:
            console.print("[red]Error: Las entradas y salidas no pueden ser negativas.[/red]")
            return
        
        auto_generator = Autos()
        
        # Procesar salidas primero
        salidas_exitosas = 0
        for i in range(min(salidas, len(autos_estacionados))):
            if autos_estacionados:
                placa = autos_estacionados.pop(0)  # FIFO
                tarifa = generar_tarifa_aleatoria()
                hora = datetime.now()
                historial.guardar_evento(placa, hora, "salida", tarifa)
                salidas_exitosas += 1
                console.print(f"[yellow]Auto {placa} salió - Tarifa: ${tarifa}[/yellow]")
        
        # Procesar entradas
        entradas_exitosas = 0
        espacios_disponibles = CAPACIDAD_MAX - len(autos_estacionados)
        
        for i in range(min(entradas, espacios_disponibles)):
            placa = auto_generator.generar_placa()
            autos_estacionados.append(placa)
            hora = datetime.now()
            historial.guardar_evento(placa, hora, "entrada")
            entradas_exitosas += 1
            console.print(f"[green]Auto {placa} entró[/green]")
        
        # Actualizar estado del parqueo
        parqueo.actualizar(len(autos_estacionados))
        
        # Usar la función de simulación de movimiento de la clase Autos
        cantidad_nueva, _, _ = auto_generator.simular_movimiento(
            len(autos_estacionados), entradas_exitosas, salidas_exitosas, CAPACIDAD_MAX
        )
        
        console.print(f"\n[bold]Resumen del ciclo:[/bold]")
        console.print(f"Entradas exitosas: {entradas_exitosas}")
        console.print(f"Salidas exitosas: {salidas_exitosas}")
        if entradas > entradas_exitosas:
            console.print(f"[red]Entradas rechazadas por capacidad: {entradas - entradas_exitosas}[/red]")
        if salidas > salidas_exitosas:
            console.print(f"[red]Salidas no realizadas (no había suficientes autos): {salidas - salidas_exitosas}[/red]")
        
        mostrar_estado_resumido()
        
    except Exception as e:
        console.print(f"[red]Error en la simulación: {str(e)}[/red]")

def mostrar_estado_resumido():
    """Muestra un resumen rápido del estado actual"""
    estado = parqueo.resumen()
    nivel_color = {
        "BAJO": "green",
        "MEDIO": "yellow", 
        "ALTO": "orange1",
        "LLENO": "red"
    }.get(estado['nivel'], "white")
    
    console.print(f"\n[bold]Estado: [/bold][{nivel_color}]{estado['ocupados']}/{estado['capacidad']} ocupados ({estado['porcentaje']}%) - {estado['nivel']}[/{nivel_color}]")

def ver_estado():
    estado = parqueo.resumen()
    
    # Determinar color según el nivel
    nivel_color = {
        "BAJO": "green",
        "MEDIO": "yellow",
        "ALTO": "orange1", 
        "LLENO": "red"
    }.get(estado['nivel'], "white")
    
    panel_text = (
        f"[bold]Capacidad:[/bold] {estado['capacidad']}\n"
        f"[bold]Ocupados:[/bold] {estado['ocupados']}\n"
        f"[bold]Libres:[/bold] {estado['libres']}\n"
        f"[bold]Porcentaje:[/bold] {estado['porcentaje']}%\n"
        f"[bold]Nivel:[/bold] [{nivel_color}]{estado['nivel']}[/{nivel_color}]\n"
        f"[bold]Pueden entrar:[/bold] {estado['pueden_entrar']}\n\n"
        f"{parqueo.gauge_ascii(30)}"
    )
    console.print(Panel(panel_text, title="Estado Actual del Parqueo", expand=False))

def ver_autos_estacionados():
    """Muestra todos los autos que están actualmente estacionados"""
    console.print(Panel("[bold cyan]Autos Actualmente Estacionados[/bold cyan]", expand=False))
    
    if not autos_estacionados:
        console.print("[yellow]No hay autos estacionados actualmente.[/yellow]")
        return
    
    table = Table(title="Vehículos en el Parqueo", show_lines=True)
    table.add_column("N°", style="cyan", justify="center")
    table.add_column("Placa", style="green", justify="center")
    table.add_column("Estado", style="blue")
    
    for i, placa in enumerate(autos_estacionados, 1):
        table.add_row(str(i), placa, "Estacionado")
    
    console.print(table)
    console.print(f"\n[bold]Total de autos estacionados: {len(autos_estacionados)}/{CAPACIDAD_MAX}[/bold]")

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
            tarifa_str = f"${tarifa:.2f}" if tipo == "salida" and tarifa > 0 else "-"
            table.add_row(placa_ev, hora.strftime("%Y-%m-%d %H:%M:%S"), tipo, tarifa_str)
    else:
        todos = historial.obtener_todos()
        if not todos:
            console.print("[yellow]No hay eventos registrados aún.[/yellow]")
            return
        for placa_ev, lista in todos.items():
            for ev in lista:
                placa_ev, hora, tipo, tarifa = ev
                tarifa_str = f"${tarifa:.2f}" if tipo == "salida" and tarifa > 0 else "-"
                table.add_row(placa_ev, hora.strftime("%Y-%m-%d %H:%M:%S"), tipo, tarifa_str)
    console.print(table)

def simulacion_automatica():
    """Ejecuta una simulación automática aleatoria"""
    console.print(Panel("[bold magenta]Simulación Automática Aleatoria[/bold magenta]", expand=False))
    
    ciclos = IntPrompt.ask("¿Cuántos ciclos de simulación desea ejecutar?", default=5)
    
    for i in range(ciclos):
        console.print(f"\n[bold blue]--- Ciclo {i+1} ---[/bold blue]")
        
        # Generar números aleatorios de entradas y salidas
        max_entradas = min(3, CAPACIDAD_MAX - len(autos_estacionados))
        max_salidas = min(3, len(autos_estacionados))
        
        entradas = random.randint(0, max_entradas) if max_entradas > 0 else 0
        salidas = random.randint(0, max_salidas) if max_salidas > 0 else 0
        
        console.print(f"Simulando {entradas} entradas y {salidas} salidas...")
        
        auto_generator = Autos()
        
        # Procesar salidas
        for j in range(salidas):
            if autos_estacionados:
                placa = autos_estacionados.pop(0)
                tarifa = generar_tarifa_aleatoria()
                hora = datetime.now()
                historial.guardar_evento(placa, hora, "salida", tarifa)
        
        # Procesar entradas
        for j in range(entradas):
            if len(autos_estacionados) < CAPACIDAD_MAX:
                placa = auto_generator.generar_placa()
                autos_estacionados.append(placa)
                hora = datetime.now()
                historial.guardar_evento(placa, hora, "entrada")
        
        # Actualizar estado
        parqueo.actualizar(len(autos_estacionados))
        mostrar_estado_resumido()
        
        # Pausa entre ciclos
        if i < ciclos - 1:
            console.input("[dim]Presione Enter para continuar al siguiente ciclo...[/dim]")
    
    console.print("\n[bold green]¡Simulación automática completada![/bold green]")

def main():
    while True:
        mostrar_menu()
        try:
            opcion = Prompt.ask(
                "[bold white]Seleccione una opción[/bold white]", 
                choices=["1", "2", "3", "4", "5", "6", "7", "8"]
            )
            
            if opcion == "1":
                simular_entrada()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "2":
                simular_salida()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "3":
                simulacion_por_ciclos()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "4":
                ver_estado()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "5":
                ver_autos_estacionados()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "6":
                ver_historial()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "7":
                simulacion_automatica()
                console.input("[cyan]Presione Enter para continuar...[/cyan]")
            elif opcion == "8":
                console.print(Panel("[bold green]¡Hasta luego![/bold green]", expand=False))
                break
        except KeyboardInterrupt:
            console.print("\n[yellow]Operación cancelada por el usuario.[/yellow]")
            console.input("[cyan]Presione Enter para continuar...[/cyan]")
        except Exception as e:
            console.print(f"[red]Error inesperado: {str(e)}[/red]")
            console.input("[cyan]Presione Enter para continuar...[/cyan]")

if __name__ == "__main__":
    main()