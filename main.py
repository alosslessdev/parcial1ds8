# main.py
try:
    import config
    import autos
    import estado
    import eventos
except ImportError:
    print("Algunos módulos aún no están listos. ")

def mostrar_menu():
    print("\n--- Sistema de Parqueo ---")
    print("1. Simular entrada de autos")
    print("2. Simular salida de autos")
    print("3. Ver estado del parqueo")
    print("4. Ver historial de eventos")
    print("5. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            # Aquí deberás llamar a la función para simular entrada de autos
            print("Función de entrada de autos (a implementar)")
        elif opcion == "2":
            # Aquí deberás llamar a la función para simular salida de autos
            print("Función de salida de autos (a implementar)")
        elif opcion == "3":
            # Aquí deberás mostrar el estado del parqueo
            print("Función de estado del parqueo (a implementar)")
        elif opcion == "4":
            # Aquí deberás mostrar el historial de eventos
            print("Función de historial de eventos (a implementar)")
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()