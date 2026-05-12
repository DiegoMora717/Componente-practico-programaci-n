# PERSONA 3 - CLASE RESERVA


class ReservaError(Exception):
    pass


class Reserva:

    # CONSTRUCTOR
    def __init__(self, cliente, servicio, duracion):

        try:
            # Validar cliente
            if cliente is None:
                raise ReservaError("El cliente no puede ser nulo.")

            # Validar servicio
            if servicio is None:
                raise ReservaError("El servicio no puede ser nulo.")

            # Validar duración
            if not isinstance(duracion, (int, float)):
                raise ReservaError("La duración debe ser numérica.")

            if duracion <= 0:
                raise ReservaError("La duración debe ser mayor que cero.")

        except ReservaError as e:
            # Registro del error en archivo
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(f"ERROR CREANDO RESERVA: {e}\n")
            raise

        else:
            # Asignación de atributos
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "Pendiente"

            # Conexión con cliente
            try:
                cliente.agregar_reserva(self)

            except Exception as e:
                with open("logs.txt", "a", encoding="utf-8") as log:
                    log.write(f"ERROR AGREGANDO RESERVA AL CLIENTE: {e}\n")

                raise ReservaError(
                    "No fue posible asociar la reserva al cliente."
                ) from e

            # Registrar evento exitoso
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(
                    f"RESERVA CREADA: Cliente={cliente.nombre}, "
                    f"Servicio={servicio.nombre}, "
                    f"Duración={duracion}, Estado=Pendiente\n"
                )

        finally:
            print("Proceso de creación de reserva finalizado.")

    # CONFIRMAR
    def confirmar(self):

        try:
            # No permitir confirmar reserva cancelada
            if self.estado == "Cancelada":
                raise ReservaError(
                    "No se puede confirmar una reserva cancelada."
                )

            # Validar disponibilidad del servicio
            if hasattr(self.servicio, "disponible"):
                if not self.servicio.disponible:
                    raise ReservaError(
                        "El servicio no se encuentra disponible."
                    )

        except ReservaError as e:
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(f"ERROR CONFIRMANDO RESERVA: {e}\n")
            raise

        else:
            self.estado = "Confirmada"

            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(
                    f"RESERVA CONFIRMADA: Cliente={self.cliente.nombre}, "
                    f"Servicio={self.servicio.nombre}\n"
                )

            print(f"Reserva confirmada para {self.cliente.nombre}")

        finally:
            print("Proceso de confirmación finalizado.")

    # CANCELAR
    def cancelar(self):

        try:
            if self.estado == "Cancelada":
                raise ReservaError("La reserva ya fue cancelada.")

        except ReservaError as e:
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(f"ERROR CANCELANDO RESERVA: {e}\n")
            raise

        else:
            self.estado = "Cancelada"

            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(
                    f"RESERVA CANCELADA: Cliente={self.cliente.nombre}, "
                    f"Servicio={self.servicio.nombre}\n"
                )

            print(f"Reserva cancelada para {self.cliente.nombre}")

        finally:
            print("Proceso de cancelación finalizado.")

    # CALCULAR TOTAL
    def calcular_total(self, impuesto=0, descuento=0):

        try:
            # No calcular si está cancelada
            if self.estado == "Cancelada":
                raise ReservaError(
                    "No se puede calcular una reserva cancelada."
                )

            # Verificar que el servicio tenga calcular_costo
            if not hasattr(self.servicio, "calcular_costo"):
                raise ReservaError(
                    "El servicio no implementa calcular_costo."
                )

            # Calcular costo base
            costo_base = self.servicio.calcular_costo(self.duracion)

            # Validar costo
            if costo_base < 0:
                raise ReservaError(
                    "El costo base no puede ser negativo."
                )

        except ReservaError as e:
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(f"ERROR CALCULANDO TOTAL: {e}\n")
            raise

        except Exception as e:
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(f"ERROR GENERAL EN CÁLCULO: {e}\n")

            raise ReservaError(
                "Error inesperado en el cálculo."
            ) from e

        else:
            # Aplicar descuento
            total = costo_base - (costo_base * descuento / 100)

            # Aplicar impuesto
            total += total * impuesto / 100

            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(
                    f"CÁLCULO TOTAL: Cliente={self.cliente.nombre}, "
                    f"Base={costo_base}, Impuesto={impuesto}%, "
                    f"Descuento={descuento}%, Total={total}\n"
                )

            return total

        finally:
            print("Proceso de cálculo finalizado.")

    # MOSTRAR DETALLE
    def mostrar_reserva(self):

        try:
            print("===== DETALLE DE RESERVA =====")
            print(f"Cliente: {self.cliente.nombre}")
            print(f"Servicio: {self.servicio.nombre}")
            print(f"Duración: {self.duracion}")
            print(f"Estado: {self.estado}")
            print(f"Total: ${self.calcular_total():,.2f}")

        except Exception as e:
            with open("logs.txt", "a", encoding="utf-8") as log:
                log.write(f"ERROR MOSTRANDO RESERVA: {e}\n")

            raise ReservaError(
                "No fue posible mostrar la reserva."
            ) from e

        
