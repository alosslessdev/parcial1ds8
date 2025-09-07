from __future__ import annotations# Permite anotaciones de tipo futuras (Python 3.7+)
from dataclasses import dataclass# Para definir clases de datos inmutables
from enum import Enum # Para definir enumeraciones
from typing import Optional # Para tipos opcionales


# -----------------------------
# Enumeración para los niveles de ocupación
# -----------------------------
class NivelOcupacion(Enum):
    BAJO = "BAJO"      # Ocupación baja
    MEDIO = "MEDIO"    # Ocupación media
    ALTO = "ALTO"      # Ocupación alta
    LLENO = "LLENO"    # Parqueo lleno


# -----------------------------
# Clase que define los umbrales de ocupación
# -----------------------------
@dataclass(frozen=True) 
class UmbralesOcupacion:
    """
    Define los puntos de corte de ocupación en proporciones (0.0 a 1.0).

    medio: todo lo que sea <= medio es BAJO
    alto:  todo lo que esté entre medio y alto es MEDIO
           todo lo que esté > alto y < 1 es ALTO
           1.0 o más es LLENO
    """
    medio: float = 0.50  # 50% del parqueo
    alto: float = 0.80   # 80% del parqueo

    def validar(self) -> None:
        """Verifica que los umbrales sean válidos."""
        if not (0 < self.medio < self.alto < 1):
            raise ValueError("Umbrales inválidos: se espera 0 < medio < alto < 1.")


# -----------------------------
# Clase principal que calcula y expone el estado del parqueo
# -----------------------------
class EstadoParqueo:
    """
    Calcula y muestra el estado del parqueo según:
    - Capacidad máxima
    - Autos actualmente ocupando
    - Umbrales de ocupación
    """

    def __init__(self, capacidad_max: int,
                 umbrales: Optional[UmbralesOcupacion] = None,
                 clamp: bool = True) -> None:
        """
        Inicializa el parqueo.
        :param capacidad_max: número máximo de autos que caben
        :param umbrales: umbrales personalizados (opcional)
        :param clamp: si True, limita ocupación entre 0 y capacidad_max
        """
        if capacidad_max <= 0:
            raise ValueError("capacidad_max debe ser > 0")

        self.capacidad_max = int(capacidad_max)               # capacidad máxima del parqueo
        self.umbrales = umbrales or UmbralesOcupacion()       # usa umbrales por defecto si no se pasan
        self.umbrales.validar()                               # valida que los umbrales sean correctos
        self._ocupados = 0                                    # cantidad de autos dentro
        self._clamp = clamp                                   # si se fuerza a estar dentro de rango

    # --------- Métodos de actualización y acceso básico ----------
    def actualizar(self, ocupados: int) -> None:
        """
        Actualiza el número de autos ocupados en el parqueo.
        """
        if ocupados < 0:
            raise ValueError("ocupados no puede ser negativo")

        if self._clamp:
            # Se limita el valor entre 0 y la capacidad máxima
            self._ocupados = max(0, min(int(ocupados), self.capacidad_max)) #max no menor de 0, min no mayor de max
        else:
            if ocupados > self.capacidad_max:
                raise ValueError("ocupados excede la capacidad máxima")
            self._ocupados = int(ocupados)

    @property
    def ocupados(self) -> int:
        """Devuelve cuántos autos están ocupando espacio."""
        return self._ocupados

    @property
    def libres(self) -> int:
        """Devuelve cuántos espacios aún están disponibles."""
        return self.capacidad_max - self._ocupados

    # --------- Cálculos principales ----------
    @property
    def ratio(self) -> float:
        """Devuelve la proporción de ocupación (entre 0.0 y 1.0)."""
        return 0.0 if self.capacidad_max == 0 else self._ocupados / self.capacidad_max

    @property
    def porcentaje(self) -> float:
        """Devuelve el porcentaje de ocupación con 2 decimales."""
        return round(self.ratio * 100.0, 2)

    @property
    def nivel(self) -> NivelOcupacion:
        """Clasifica el nivel de ocupación según los umbrales."""
        r = self.ratio
        if r >= 1.0:
            return NivelOcupacion.LLENO
        if r > self.umbrales.alto:
            return NivelOcupacion.ALTO
        if r > self.umbrales.medio:
            return NivelOcupacion.MEDIO
        return NivelOcupacion.BAJO

    def cuantos_pueden_entrar(self) -> int:
        """Devuelve cuántos autos aún podrían entrar."""
        return max(0, self.capacidad_max - self._ocupados)

    def puede_admitir(self, n: int = 1) -> bool:
        """
        Verifica si el parqueo puede admitir n autos más.
        """
        if n < 0:
            raise ValueError("n no puede ser negativo")
        return self._ocupados + n <= self.capacidad_max

    # --------- Representaciones amigables ----------
    def resumen(self) -> dict:
        """
        Devuelve un resumen del estado en forma de diccionario.
        Ideal para integrarlo con el resto del sistema.
        """
        return {
            "capacidad": self.capacidad_max,
            "ocupados": self.ocupados,
            "libres": self.libres,
            "porcentaje": self.porcentaje,
            "nivel": self.nivel.value,
            "pueden_entrar": self.cuantos_pueden_entrar(),
        }

    def linea_estado(self) -> str:
        """
        Devuelve una línea de texto con toda la información del parqueo.
        """
        return (f"[Parqueo] Ocupados: {self.ocupados}/{self.capacidad_max}  "
                f"Libres: {self.libres}  Ocupación: {self.porcentaje}%  "
                f"Nivel: {self.nivel.value}")

    def gauge_ascii(self, width: int = 20) -> str:
        """
        Dibuja una barra de progreso ASCII para representar visualmente
        el nivel de ocupación.
        :param width: ancho total de la barra
        """
        width = max(5, width)  # mínimo ancho para la barra
        filled = int(round(self.ratio * width))  # cuántos bloques se llenan
        bar = "#" * filled + "-" * (width - filled)
        return f"[{bar}] {self.porcentaje}%"


# -----------------------------
# Ejemplo de uso (pruebas rápidas)
# -----------------------------
if __name__ == "__main__":
    estado = EstadoParqueo(capacidad_max=10)

    # Probar diferentes ocupaciones
    for ocup in (0, 3, 5, 8, 10):
        estado.actualizar(ocup)
        print(estado.linea_estado(), estado.gauge_ascii())
