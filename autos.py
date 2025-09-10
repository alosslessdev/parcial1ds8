import random
import string

class Autos:
    def __init__(self):
        self.placa = self.generar_placa()

    #getters y setters
    def get_placa(self):
        return self.placa
    def set_placa(self, placa):
        self.placa = placa

    def generar_placa(self):
        # Genera una placa aleatoria en el formato ABC-123
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        numeros = ''.join(random.choices(string.digits, k=3))
        return f"{letras}-{numeros}"
    
    def guardar_placa(self, lista_placa):
        # Guarda la placa en una lista que se pasa como argumento
        return lista_placa.append(self.placa)
    
    def mostrar_placas(self, lista_placas):
        # Muestra las placas guardadas en la lista que se pasa como argumento
        placas_str = ', '.join(lista_placas)
        return placas_str
    
    def simular_movimiento(self, cantidad_actual, entradas, salidas, capacidad_max):
        """
        Maneja el ciclo de simulación de autos que entran y salen.
        Retorna la cantidad actualizada de autos en el parqueo, entradas y salidas totales.
        Maneja errores de entrada de datos.
        """
        try:
            if not all(isinstance(x, int) for x in [cantidad_actual, entradas, salidas, capacidad_max]):
                raise TypeError("Todos los parámetros deben ser enteros.")
            if capacidad_max < 0:
                raise ValueError("La capacidad máxima no puede ser negativa.")
            if entradas < 0 or salidas < 0:
                raise ValueError("Las entradas y salidas no pueden ser negativas.")
            cantidad_nueva = cantidad_actual + entradas - salidas # Calcular nueva cantidad
            cantidad_nueva = max(0, min(cantidad_nueva, capacidad_max)) # Clamp entre 0 y capacidad_max
            entradas_totales = entradas
            salidas_totales = salidas 
            return cantidad_nueva, entradas_totales, salidas_totales
        except Exception as e:
            return f"Error: {str(e)}", 0, 0 # Retorna 0 en entradas y salidas en caso de error

    