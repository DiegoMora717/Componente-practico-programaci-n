# =============================================================================
# MÓDULO: excepciones.py
# DESCRIPCIÓN: Todas las excepciones personalizadas y funciones de log
# =============================================================================

from datetime import datetime

# ---------------------------------------------------------------------------
# EXCEPCIONES CLIENTE
# ---------------------------------------------------------------------------

class ClienteError(Exception):
    pass

# ---------------------------------------------------------------------------
# EXCEPCIONES RESERVA
# ---------------------------------------------------------------------------

class ReservaError(Exception):
    pass

# ---------------------------------------------------------------------------
# EXCEPCIONES SERVICIO
# ---------------------------------------------------------------------------

class ServicioError(Exception):
    pass

class ServicioNoDisponibleError(ServicioError):
    def __init__(self, servicio):
        super().__init__(f"El servicio '{servicio}' no está disponible.")

class ServicioCapacidadError(ServicioError):
    def __init__(self, capacidad):
        super().__init__(f"Capacidad inválida: {capacidad}")

class ServicioCostoError(ServicioError):
    def __init__(self, costo):
        super().__init__(f"Costo inválido: {costo}")

# ---------------------------------------------------------------------------
# FUNCIONES DE LOG  — archivo único: errores.log
# ---------------------------------------------------------------------------

ARCHIVO_LOG = "errores.log"

def registrar_error(error):
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"[ERROR] {datetime.now()} - {error}\n")

def registrar_info(mensaje):
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"[INFO]  {datetime.now()} - {mensaje}\n")
