# eventos.py
from datetime import datetime

class HistorialEventos:
    def __init__(self):
        # Diccionario donde la clave es la placa y el valor es una lista de eventos
        self.historial = {}

    def guardar_evento(self, placa: str, hora: datetime, tipo: str, tarifa: float = 0.0):
        """
        Guarda un evento en el historial.
        
        :param placa: Número de placa del vehículo
        :param hora: Fecha y hora del evento (datetime)
        :param tipo: 'entrada' o 'salida'
        :param tarifa: Costo asociado (solo aplica en salida normalmente)
        """
        evento = (placa, hora, tipo, tarifa)
        
        if placa not in self.historial:
            self.historial[placa] = []
        
        self.historial[placa].append(evento)

    def obtener_historial(self, placa: str):
        """
        Devuelve la lista de eventos de una placa.
        """
        return self.historial.get(placa, [])

    def obtener_todos(self):
        """
        Devuelve el historial completo de todos los vehículos.
        """
        return self.historial
