# =============================================================================
# MÓDULO: servicio.py
# DESCRIPCIÓN: Clase abstracta Servicio y sus tres subclases especializadas
# AUTOR: Gustavo Romero - Servicio (Clase Madre)
# =============================================================================

from abc import ABC, abstractmethod

# CORRECCIÓN 4: Se reemplaza 'from logger import ...' por 'from excepciones import ...'
#               El módulo logger no existe; registrar_error y registrar_info
#               están definidos en excepciones.py.
from excepciones import (
    ServicioNoDisponibleError,
    ServicioCapacidadError,
    ServicioCostoError,
    registrar_error,
    registrar_info
)


# =============================================================================
# CLASE ABSTRACTA BASE
# =============================================================================

class Servicio(ABC):
    """
    Clase abstracta que representa un servicio genérico de Software FJ.
    No se puede instanciar directamente; obliga a las subclases a implementar
    calcular_costo() y descripcion().
    """

    def __init__(self, nombre: str, costo_base: float):
        if not nombre or not nombre.strip():
            raise ServicioCostoError("El nombre del servicio no puede estar vacío")
        if not isinstance(costo_base, (int, float)) or costo_base <= 0:
            raise ServicioCostoError(costo_base)

        self._nombre = nombre.strip()
        self._costo_base = float(costo_base)
        self._disponible = True

    # -------------------------------------------------------------------------
    # MÉTODOS ABSTRACTOS
    # -------------------------------------------------------------------------

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass

    # -------------------------------------------------------------------------
    # MÉTODOS CONCRETOS
    # -------------------------------------------------------------------------

    def verificar_disponibilidad(self) -> bool:
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)
        return True

    def _calcular_con_ajustes(self, costo_bruto: float, impuesto: float, descuento: float) -> float:
        """Aplica descuento e impuesto al costo bruto."""
        costo_con_descuento = costo_bruto * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return round(costo_final, 2)

    # -------------------------------------------------------------------------
    # PROPIEDADES
    # -------------------------------------------------------------------------

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"{self._nombre} | Costo base: ${self._costo_base:,.0f} | {estado}"


# =============================================================================
# SUBCLASE 1: RESERVA DE SALA  (cobra por HORA)
# =============================================================================

class ServicioSala(Servicio):

    def __init__(self, nombre: str, costo_base: float, capacidad: int):
        super().__init__(nombre, costo_base)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioCapacidadError(capacidad)
        self._capacidad = capacidad
        registrar_info(f"ServicioSala creado: {nombre} | Capacidad: {capacidad} personas")

    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        self.verificar_disponibilidad()
        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}")
        return self._calcular_con_ajustes(self._costo_base * duracion, impuesto, descuento)

    def descripcion(self) -> str:
        return (f"SALA: {self._nombre} | Capacidad: {self._capacidad} personas | "
                f"${self._costo_base:,.0f}/hora | {'Disponible' if self._disponible else 'No disponible'}")

    @property
    def capacidad(self) -> int:
        return self._capacidad


# =============================================================================
# SUBCLASE 2: ALQUILER DE EQUIPO  (cobra por DÍA)
# =============================================================================

class ServicioEquipo(Servicio):

    def __init__(self, nombre: str, costo_base: float, tipo_equipo: str):
        super().__init__(nombre, costo_base)
        if not tipo_equipo or not tipo_equipo.strip():
            raise ServicioCostoError("El tipo de equipo no puede estar vacío")
        self._tipo_equipo = tipo_equipo.strip()
        registrar_info(f"ServicioEquipo creado: {nombre} | Tipo: {tipo_equipo}")

    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        self.verificar_disponibilidad()
        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}")
        return self._calcular_con_ajustes(self._costo_base * duracion, impuesto, descuento)

    def descripcion(self) -> str:
        return (f"EQUIPO: {self._nombre} | Tipo: {self._tipo_equipo} | "
                f"${self._costo_base:,.0f}/día | {'Disponible' if self._disponible else 'No disponible'}")

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo


# =============================================================================
# SUBCLASE 3: ASESORÍA ESPECIALIZADA  (cobra por SESIÓN)
# =============================================================================

class ServicioAsesoria(Servicio):

    def __init__(self, nombre: str, costo_base: float, especialidad: str, sesiones_disponibles: int = 10):
        super().__init__(nombre, costo_base)
        if not especialidad or not especialidad.strip():
            raise ServicioCostoError("La especialidad no puede estar vacía")
        if not isinstance(sesiones_disponibles, int) or sesiones_disponibles < 0:
            raise ServicioCapacidadError(sesiones_disponibles)
        self._especialidad = especialidad.strip()
        self._sesiones_disponibles = sesiones_disponibles
        registrar_info(f"ServicioAsesoria creado: {nombre} | Especialidad: {especialidad}")

    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        self.verificar_disponibilidad()
        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}")
        if duracion > self._sesiones_disponibles:
            raise ServicioNoDisponibleError(
                f"{self._nombre} — Solo quedan {self._sesiones_disponibles} sesiones"
            )
        return self._calcular_con_ajustes(self._costo_base * duracion, impuesto, descuento)

    def descripcion(self) -> str:
        return (f"ASESORÍA: {self._nombre} | {self._especialidad} | "
                f"${self._costo_base:,.0f}/sesión | Sesiones: {self._sesiones_disponibles}")

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @property
    def sesiones_disponibles(self) -> int:
        return self._sesiones_disponibles
