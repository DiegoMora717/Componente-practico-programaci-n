# =============================================================================
# MÓDULO: reservas.py
# DESCRIPCIÓN: Clase Reserva — conecta Cliente con Servicio
# =============================================================================

# CORRECCIÓN 5: Se elimina la definición duplicada de ReservaError.
#               Ahora se importa desde excepciones.py (módulo centralizado).
# CORRECCIÓN 6: Se reemplaza el archivo de log 'logs.txt' por 'errores.log'
#               para usar el archivo único definido en excepciones.py.
from excepciones import ReservaError, registrar_error, registrar_info


class Reserva:
    """
    Representa una reserva en el sistema Software FJ.
    Une un Cliente con un Servicio y gestiona su ciclo de vida:
    Pendiente → Confirmada / Cancelada.
    """

    def __init__(self, cliente, servicio, duracion):
        try:
            if cliente is None:
                raise ReservaError("El cliente no puede ser nulo.")
            if servicio is None:
                raise ReservaError("El servicio no puede ser nulo.")
            if not isinstance(duracion, (int, float)):
                raise ReservaError("La duración debe ser numérica.")
            if duracion <= 0:
                raise ReservaError("La duración debe ser mayor que cero.")

        except ReservaError as e:
            registrar_error(f"Error creando reserva: {e}")
            raise

        else:
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "Pendiente"

            try:
                # CORRECCIÓN 7: cliente.nombre ahora funciona gracias a la
                #               propiedad @property agregada en cliente.py.
                cliente.agregar_reserva(self)
            except Exception as e:
                registrar_error(f"Error agregando reserva al cliente: {e}")
                raise ReservaError("No fue posible asociar la reserva al cliente.") from e

            registrar_info(
                f"Reserva creada | Cliente: {cliente.nombre} | "
                f"Servicio: {servicio.nombre} | Duración: {duracion} | Estado: Pendiente"
            )

        finally:
            print("  → Proceso de creación de reserva finalizado.")

    # -------------------------------------------------------------------------
    # CONFIRMAR
    # -------------------------------------------------------------------------

    def confirmar(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaError("No se puede confirmar una reserva cancelada.")
            if self.estado == "Confirmada":
                raise ReservaError("La reserva ya está confirmada.")
            if hasattr(self.servicio, "disponible") and not self.servicio.disponible:
                raise ReservaError("El servicio no se encuentra disponible.")

        except ReservaError as e:
            registrar_error(f"Error confirmando reserva: {e}")
            raise

        else:
            self.estado = "Confirmada"
            registrar_info(f"Reserva confirmada | Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre}")
            print(f"  → Reserva confirmada para {self.cliente.nombre}")

        finally:
            print("  → Proceso de confirmación finalizado.")

    # -------------------------------------------------------------------------
    # CANCELAR
    # -------------------------------------------------------------------------

    def cancelar(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaError("La reserva ya fue cancelada.")

        except ReservaError as e:
            registrar_error(f"Error cancelando reserva: {e}")
            raise

        else:
            self.estado = "Cancelada"
            registrar_info(f"Reserva cancelada | Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre}")
            print(f"  → Reserva cancelada para {self.cliente.nombre}")

        finally:
            print("  → Proceso de cancelación finalizado.")

    # -------------------------------------------------------------------------
    # CALCULAR TOTAL
    # -------------------------------------------------------------------------

    def calcular_total(self, impuesto=0, descuento=0):
        try:
            if self.estado == "Cancelada":
                raise ReservaError("No se puede calcular una reserva cancelada.")
            if not hasattr(self.servicio, "calcular_costo"):
                raise ReservaError("El servicio no implementa calcular_costo.")

            costo_base = self.servicio.calcular_costo(self.duracion)
            if costo_base < 0:
                raise ReservaError("El costo base no puede ser negativo.")

        except ReservaError as e:
            registrar_error(f"Error calculando total: {e}")
            raise

        except Exception as e:
            registrar_error(f"Error general en cálculo: {e}")
            raise ReservaError("Error inesperado en el cálculo.") from e

        else:
            total = costo_base - (costo_base * descuento / 100)
            total += total * impuesto / 100
            registrar_info(
                f"Cálculo total | Cliente: {self.cliente.nombre} | "
                f"Base: ${costo_base:,.0f} | Impuesto: {impuesto}% | "
                f"Descuento: {descuento}% | Total: ${total:,.0f}"
            )
            return total

        finally:
            print("  → Proceso de cálculo finalizado.")

    # -------------------------------------------------------------------------
    # MOSTRAR DETALLE
    # -------------------------------------------------------------------------

    def mostrar_reserva(self):
        try:
            total = self.calcular_total()
            print("  ===== DETALLE DE RESERVA =====")
            print(f"  Cliente:  {self.cliente.nombre}")
            print(f"  Servicio: {self.servicio.nombre}")
            print(f"  Duración: {self.duracion}")
            print(f"  Estado:   {self.estado}")
            print(f"  Total:    ${total:,.0f} COP")
        except Exception as e:
            registrar_error(f"Error mostrando reserva: {e}")
            raise ReservaError("No fue posible mostrar la reserva.") from e
