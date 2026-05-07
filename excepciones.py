
# MÓDULO: excepciones.py

from datetime import datetime

# EXCEPCIONES CLIENTE

class ClienteError(Exception):
    pass

# EXCEPCIONES RESERVA


class ReservaError(Exception):
    pass

# EXCEPCIONES SERVICIO


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


# FUNCIONES DE LOGS


def registrar_error(error):

    with open("errores.log", "a", encoding="utf-8") as archivo:
        archivo.write(
            f"[ERROR] {datetime.now()} - {error}\n"
        )


def registrar_info(mensaje):

    with open("errores.log", "a", encoding="utf-8") as archivo:
        archivo.write(
            f"[INFO] {datetime.now()} - {mensaje}\n"
        )
