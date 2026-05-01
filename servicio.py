# =============================================================================
# MÓDULO: servicio.py
# DESCRIPCIÓN: Clase abstracta Servicio y sus tres subclases especializadas
# AUTOR: Gustavo Romero - Servicio (Clase Madre)
# =============================================================================

from abc import ABC, abstractmethod  # Para definir clases y métodos abstractos
from excepciones import (
    ServicioNoDisponibleError,
    ServicioCapacidadError,
    ServicioCostoError
)
from logger import registrar_error, registrar_info


# =============================================================================
# CLASE ABSTRACTA BASE
# =============================================================================

class Servicio(ABC):
    """
    Clase abstracta que representa un servicio genérico de Software FJ.

    Al ser abstracta (ABC), NO se puede instanciar directamente.
    Obliga a sus subclases a implementar los métodos abstractos.

    Atributos:
        _nombre (str): Nombre del servicio
        _costo_base (float): Precio base por unidad de tiempo
        _disponible (bool): Si el servicio está disponible para reservar
    """

    def __init__(self, nombre: str, costo_base: float):
        """
        Constructor de la clase abstracta Servicio.

        Parámetros:
            nombre (str): Nombre descriptivo del servicio
            costo_base (float): Precio base (debe ser mayor a 0)
        """
        # Validamos que el nombre no esté vacío
        if not nombre or not nombre.strip():
            raise ServicioCostoError("El nombre del servicio no puede estar vacío")

        # Validamos que el costo base sea positivo
        if not isinstance(costo_base, (int, float)) or costo_base <= 0:
            raise ServicioCostoError(costo_base)

        self._nombre = nombre.strip()
        self._costo_base = float(costo_base)
        self._disponible = True  # Por defecto todos los servicios están disponibles

    # =========================================================================
    # MÉTODOS ABSTRACTOS — las subclases DEBEN implementarlos
    # =========================================================================

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        """
        Calcula el costo total del servicio.

        Parámetros:
            duracion (float): Unidades de tiempo (horas, días o sesiones)
            impuesto (float): Porcentaje de impuesto a aplicar (ej: 0.19 para 19%)
            descuento (float): Porcentaje de descuento a aplicar (ej: 0.10 para 10%)

        Retorna:
            float: Costo total calculado
        """
        pass  # Las subclases implementan este método

    @abstractmethod
    def descripcion(self) -> str:
        """
        Retorna una descripción detallada del servicio.

        Retorna:
            str: Texto descriptivo del servicio
        """
        pass  # Las subclases implementan este método

    # =========================================================================
    # MÉTODOS CONCRETOS — disponibles para todas las subclases
    # =========================================================================

    def verificar_disponibilidad(self) -> bool:
        """Verifica si el servicio está disponible. Lanza excepción si no lo está."""
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)
        return True

    def _calcular_con_ajustes(self, costo_bruto: float, impuesto: float, descuento: float) -> float:
        """
        Método auxiliar que aplica impuesto y descuento a un costo bruto.
        Es un método interno (prefijo _) usado por las subclases.

        Parámetros:
            costo_bruto (float): Costo antes de ajustes
            impuesto (float): Porcentaje de impuesto (0 a 1)
            descuento (float): Porcentaje de descuento (0 a 1)
        """
        # Aplicamos descuento primero
        costo_con_descuento = costo_bruto * (1 - descuento)

        # Luego aplicamos el impuesto
        costo_final = costo_con_descuento * (1 + impuesto)

        return round(costo_final, 2)

    @property
    def nombre(self) -> str:
        """Getter del nombre del servicio."""
        return self._nombre

    @property
    def costo_base(self) -> float:
        """Getter del costo base del servicio."""
        return self._costo_base

    @property
    def disponible(self) -> bool:
        """Getter del estado de disponibilidad."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        """Setter para cambiar disponibilidad del servicio."""
        self._disponible = bool(valor)

    def __str__(self) -> str:
        """Representación legible del servicio."""
        estado = "✅ Disponible" if self._disponible else "❌ No disponible"
        return f"{self._nombre} | Costo base: ${self._costo_base:,.0f} | {estado}"


# =============================================================================
# SUBCLASE 1: RESERVA DE SALA
# =============================================================================

class ServicioSala(Servicio):
    """
    Servicio de reserva de salas de reuniones o conferencias.

    Hereda de Servicio e implementa sus métodos abstractos.
    El costo se calcula por HORA.

    Atributo adicional:
        _capacidad (int): Número máximo de personas en la sala
    """

    def __init__(self, nombre: str, costo_base: float, capacidad: int):
        """
        Constructor de ServicioSala.

        Parámetros:
            nombre (str): Nombre de la sala
            costo_base (float): Precio por hora
            capacidad (int): Capacidad máxima de personas
        """
        # Llamamos al constructor del padre (Servicio)
        super().__init__(nombre, costo_base)

        # Validamos que la capacidad sea un entero positivo
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioCapacidadError(capacidad)

        self._capacidad = capacidad
        registrar_info(f"ServicioSala creado: {nombre} | Capacidad: {capacidad} personas")

    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        """
        Calcula el costo de la sala por horas.

        Parámetros:
            duracion (float): Número de horas
            impuesto (float): Porcentaje de impuesto (ej: 0.19)
            descuento (float): Porcentaje de descuento (ej: 0.10)
        """
        # Verificamos que la sala esté disponible
        self.verificar_disponibilidad()

        # Validamos la duración
        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}")

        # Cálculo base: costo por hora × número de horas
        costo_bruto = self._costo_base * duracion

        # Aplicamos impuesto y descuento
        return self._calcular_con_ajustes(costo_bruto, impuesto, descuento)

    def descripcion(self) -> str:
        """Retorna descripción detallada de la sala."""
        return (
            f"🏢 SALA: {self._nombre}\n"
            f"   Capacidad: {self._capacidad} personas\n"
            f"   Precio por hora: ${self._costo_base:,.0f} COP\n"
            f"   Disponible: {'Sí' if self._disponible else 'No'}"
        )

    @property
    def capacidad(self) -> int:
        """Getter de la capacidad de la sala."""
        return self._capacidad


# =============================================================================
# SUBCLASE 2: ALQUILER DE EQUIPO
# =============================================================================

class ServicioEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.

    El costo se calcula por DÍA de alquiler.

    Atributo adicional:
        _tipo_equipo (str): Tipo de equipo (ej: 'proyector', 'laptop', 'cámara')
    """

    def __init__(self, nombre: str, costo_base: float, tipo_equipo: str):
        """
        Constructor de ServicioEquipo.

        Parámetros:
            nombre (str): Nombre del equipo
            costo_base (float): Precio por día
            tipo_equipo (str): Categoría del equipo
        """
        super().__init__(nombre, costo_base)

        # Validamos el tipo de equipo
        if not tipo_equipo or not tipo_equipo.strip():
            raise ServicioCostoError("El tipo de equipo no puede estar vacío")

        self._tipo_equipo = tipo_equipo.strip()
        registrar_info(f"ServicioEquipo creado: {nombre} | Tipo: {tipo_equipo}")

    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        """
        Calcula el costo del equipo por días.

        Parámetros:
            duracion (float): Número de días de alquiler
            impuesto (float): Porcentaje de impuesto
            descuento (float): Porcentaje de descuento
        """
        self.verificar_disponibilidad()

        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}")

        # Cálculo base: costo por día × número de días
        costo_bruto = self._costo_base * duracion

        return self._calcular_con_ajustes(costo_bruto, impuesto, descuento)

    def descripcion(self) -> str:
        """Retorna descripción detallada del equipo."""
        return (
            f"💻 EQUIPO: {self._nombre}\n"
            f"   Tipo: {self._tipo_equipo}\n"
            f"   Precio por día: ${self._costo_base:,.0f} COP\n"
            f"   Disponible: {'Sí' if self._disponible else 'No'}"
        )

    @property
    def tipo_equipo(self) -> str:
        """Getter del tipo de equipo."""
        return self._tipo_equipo


# =============================================================================
# SUBCLASE 3: ASESORÍA ESPECIALIZADA
# =============================================================================

class ServicioAsesoria(Servicio):
    """
    Servicio de asesoría especializada con un experto.

    El costo se calcula por SESIÓN.

    Atributos adicionales:
        _especialidad (str): Área de especialización del asesor
        _sesiones_disponibles (int): Cuántas sesiones quedan disponibles
    """

    def __init__(self, nombre: str, costo_base: float, especialidad: str, sesiones_disponibles: int = 10):
        """
        Constructor de ServicioAsesoria.

        Parámetros:
            nombre (str): Nombre del asesor o servicio
            costo_base (float): Precio por sesión
            especialidad (str): Área de especialización
            sesiones_disponibles (int): Número de sesiones disponibles (por defecto 10)
        """
        super().__init__(nombre, costo_base)

        if not especialidad or not especialidad.strip():
            raise ServicioCostoError("La especialidad no puede estar vacía")

        if not isinstance(sesiones_disponibles, int) or sesiones_disponibles < 0:
            raise ServicioCapacidadError(sesiones_disponibles)

        self._especialidad = especialidad.strip()
        self._sesiones_disponibles = sesiones_disponibles
        registrar_info(f"ServicioAsesoria creado: {nombre} | Especialidad: {especialidad}")

    def calcular_costo(self, duracion: float, impuesto: float = 0, descuento: float = 0) -> float:
        """
        Calcula el costo de las asesorías por sesiones.

        Parámetros:
            duracion (float): Número de sesiones
            impuesto (float): Porcentaje de impuesto
            descuento (float): Porcentaje de descuento
        """
        self.verificar_disponibilidad()

        if duracion <= 0:
            raise ValueError(f"La duración debe ser mayor a 0. Recibido: {duracion}")

        # Verificamos que haya suficientes sesiones disponibles
        if duracion > self._sesiones_disponibles:
            raise ServicioNoDisponibleError(
                f"{self._nombre} — Solo quedan {self._sesiones_disponibles} sesiones disponibles"
            )

        # Cálculo base: costo por sesión × número de sesiones
        costo_bruto = self._costo_base * duracion

        return self._calcular_con_ajustes(costo_bruto, impuesto, descuento)

    def descripcion(self) -> str:
        """Retorna descripción detallada de la asesoría."""
        return (
            f"🎓 ASESORÍA: {self._nombre}\n"
            f"   Especialidad: {self._especialidad}\n"
            f"   Precio por sesión: ${self._costo_base:,.0f} COP\n"
            f"   Sesiones disponibles: {self._sesiones_disponibles}\n"
            f"   Disponible: {'Sí' if self._disponible else 'No'}"
        )

    @property
    def especialidad(self) -> str:
        """Getter de la especialidad."""
        return self._especialidad

    @property
    def sesiones_disponibles(self) -> int:
        """Getter de sesiones disponibles."""
        return self._sesiones_disponibles
