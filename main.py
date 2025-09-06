import os

# Importar módulos, si no existen aún, avisar pero no detener la app
try:
    import config
    import autos
    import estado
    import eventos
except ImportError:
    print("Algunos módulos aún no están listos.")

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n--- Sistema de Parqueo ---")
    print("1. Simular entrada de autos")
    print("2. Simular salida de autos")
    print("3. Ver estado del parqueo")
    print("4. Ver historial de eventos")
    print("5. Salir")

def main():
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            # Ejemplo de llamada correcta: resultado = autos.simular_entrada()
            print("Función de entrada de autos (a implementar)")
            input("Presione Enter para continuar...")
        elif opcion == "2":
            print("Función de salida de autos (a implementar)")
            input("Presione Enter para continuar...")
        elif opcion == "3":
            # Ejemplo: estado_info = estado.obtener_estado()
            print("Función de estado del parqueo (a implementar)")
            input("Presione Enter para continuar...")
        elif opcion == "4":
            # Ejemplo: historial = eventos.obtener_historial()
            print("Función de historial de eventos (a implementar)")
            input("Presione Enter para continuar...")
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()