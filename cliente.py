# =============================================================================
# MÓDULO: cliente.py
# DESCRIPCIÓN: Clase Cliente con encapsulación, getters, setters y validaciones
# =============================================================================

#  Se elimina la definición duplicada de ClienteError.

from excepciones import ClienteError, registrar_error, registrar_info


class Cliente:
    """
    Representa a un cliente de Software FJ.
    Usa atributos privados (_) con getters y setters para encapsulación.
    """

    def __init__(self, nombre, cedula, telefono, ciudad):
        if not nombre or not cedula or not telefono or not ciudad:
            raise ValueError("No pueden haber campos vacíos")

        if not str(cedula).isdigit():
            raise ValueError("La cédula debe ser numérica")

        if not str(telefono).isdigit():
            raise ValueError("El teléfono debe ser numérico")

        if len(str(telefono)) < 7:
            raise ValueError("Teléfono demasiado corto")

        self._nombre = nombre
        self._cedula = cedula
        self._telefono = telefono
        self._ciudad = ciudad
        self._estado = "activo"
        self._reservas = []

        registrar_info(f"Cliente creado: {nombre} | Cédula: {cedula}")

    # -------------------------------------------------------------------------
    # GETTERS
    # -------------------------------------------------------------------------

    def get_nombre(self):
        return self._nombre

    def get_cedula(self):
        return self._cedula

    def get_telefono(self):
        return self._telefono

    def get_ciudad(self):
        return self._ciudad

    def get_estado(self):
        return self._estado

    def get_reservas(self):
        return self._reservas.copy()

    #  Se agrega la propiedad 'nombre' para que reservas.py
    #  pueda acceder con cliente.nombre sin AttributeError.
    @property
    def nombre(self):
        return self._nombre

    # -------------------------------------------------------------------------
    # SETTERS
    # -------------------------------------------------------------------------

    def set_estado(self, estado):
        if estado not in ["activo", "inactivo"]:
            raise ValueError("Estado inválido")
        self._estado = estado

    def set_telefono(self, telefono):
        if not str(telefono).isdigit():
            raise ValueError("Teléfono inválido")
        if len(str(telefono)) < 7:
            raise ValueError("Teléfono demasiado corto")
        self._telefono = telefono

    def set_ciudad(self, ciudad):
        if not ciudad:
            raise ValueError("Ciudad inválida")
        self._ciudad = ciudad

    # -------------------------------------------------------------------------
    # MÉTODOS
    # -------------------------------------------------------------------------

    def agregar_reserva(self, reserva):
        if self._estado != "activo":
            raise ClienteError("El cliente no está activo")
        if reserva is None:
            raise ValueError("Reserva inválida")
        self._reservas.append(reserva)

    def mostrar_datos(self):
        return (f"Nombre: {self._nombre} | Cédula: {self._cedula} | "
                f"Teléfono: {self._telefono} | Ciudad: {self._ciudad} | "
                f"Estado: {self._estado}")

    def __str__(self):
        return self.mostrar_datos()

if __name__ == "__main__":
    clientes = []
    datos_clientes = [
        ("Diego",    205205, 3112746464, "Tunja"),
        ("Paola",    400765, 3245636765, "Bogotá"),
        ("Duver",    203634, 3102314466, "Duitama"),
        ("Cristian", 678901, 320657654,  "Mosquera"),
        ("Wilmer",   893046, 300987654,  "Pereira"),
        ("Felipe",   206756, 302654546,  "Melgar"),
    ]
    for datos in datos_clientes:
        try:
            cliente = Cliente(*datos)
            clientes.append(cliente)
        except ValueError as e:
            registrar_error(f"Error al crear cliente: {e}")
    for c in clientes:
        print(c)
