# =============================================================================
# MÓDULO: main.py
# DESCRIPCIÓN: Archivo principal — simula 10 operaciones del sistema
# =============================================================================

from cliente import Cliente
from servicio import ServicioSala, ServicioEquipo, ServicioAsesoria
from reservas import Reserva
from excepciones import (
    ClienteError, ReservaError, ServicioError,
    ServicioNoDisponibleError, ServicioCapacidadError, ServicioCostoError,
    registrar_info, registrar_error
)

def sep(titulo="", ancho=60):
    print(f"\n{'='*ancho}")
    if titulo:
        print(f"  {titulo}")
        print(f"{'='*ancho}")

def ok(msg):  print(f"  ✅ {msg}")
def err(msg): print(f"  ❌ {msg}")

# =============================================================================
if __name__ == "__main__":

    sep("SISTEMA SOFTWARE FJ — Simulación de operaciones")
    registrar_info("="*40)
    registrar_info("INICIO DEL SISTEMA SOFTWARE FJ")
    registrar_info("="*40)

    # ------------------------------------------------------------------
    # OP 1: Crear cliente válido
    # ------------------------------------------------------------------
    sep("OP 1: Crear cliente válido")
    try:
        diego = Cliente("Diego", 205205, 3112746464, "Tunja")
        ok(f"Cliente creado → {diego}")
    except Exception as e:
        err(f"Error inesperado: {e}")

    # ------------------------------------------------------------------
    # OP 2: Crear cliente con cédula inválida
    # ------------------------------------------------------------------
    sep("OP 2: Crear cliente con cédula inválida")
    try:
        malo = Cliente("Carlos", "ABC123", 3001234567, "Bogotá")
        err("Debió lanzar excepción")
    except ValueError as e:
        ok(f"Excepción capturada → {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP 3: Crear cliente con nombre vacío
    # ------------------------------------------------------------------
    sep("OP 3: Crear cliente con nombre vacío")
    try:
        malo2 = Cliente("", 123456, 3009876543, "Cali")
        err("Debió lanzar excepción")
    except ValueError as e:
        ok(f"Excepción capturada → {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP 4: Crear ServicioSala válido
    # ------------------------------------------------------------------
    sep("OP 4: Crear ServicioSala válido")
    try:
        sala_a = ServicioSala("Sala Conferencias A", 150000, 20)
        ok(f"Servicio creado → {sala_a.descripcion()}")
    except Exception as e:
        err(f"Error: {e}")

    # ------------------------------------------------------------------
    # OP 5: Crear ServicioSala con capacidad negativa
    # ------------------------------------------------------------------
    sep("OP 5: Crear ServicioSala con capacidad negativa")
    try:
        sala_mala = ServicioSala("Sala X", 100000, -5)
        err("Debió lanzar excepción")
    except ServicioCapacidadError as e:
        ok(f"Excepción capturada → {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP 6: Crear ServicioEquipo y ServicioAsesoria
    # ------------------------------------------------------------------
    sep("OP 6: Crear ServicioEquipo y ServicioAsesoria")
    try:
        equipo1   = ServicioEquipo("Proyector Epson 4K", 80000, "Proyector")
        asesoria1 = ServicioAsesoria("Consultoría Software", 200000, "Ingeniería de Software", 5)
        ok(f"Equipo   → {equipo1.descripcion()}")
        ok(f"Asesoría → {asesoria1.descripcion()}")
    except Exception as e:
        err(f"Error: {e}")

    # ------------------------------------------------------------------
    # OP 7: Crear reserva exitosa y confirmarla
    # ------------------------------------------------------------------
    sep("OP 7: Crear y confirmar reserva exitosa")
    try:
        paola    = Cliente("Paola", 400765, 3245636765, "Bogotá")
        reserva1 = Reserva(paola, sala_a, 3)
        reserva1.confirmar()
        total = reserva1.calcular_total(impuesto=19, descuento=10)
        ok(f"Total con 19% IVA y 10% descuento → ${total:,.0f} COP")
    except Exception as e:
        err(f"Error: {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP 8: Intentar confirmar reserva ya confirmada
    # ------------------------------------------------------------------
    sep("OP 8: Confirmar reserva ya confirmada (debe fallar)")
    try:
        reserva1.confirmar()
        err("Debió lanzar excepción")
    except ReservaError as e:
        ok(f"Excepción capturada → {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP 9: Calcular costos con polimorfismo
    # ------------------------------------------------------------------
    sep("OP 9: Calcular costos (polimorfismo)")
    try:
        c_sala   = sala_a.calcular_costo(2, impuesto=0.19, descuento=0.10)
        c_equipo = equipo1.calcular_costo(3, impuesto=0.19)
        c_aseso  = asesoria1.calcular_costo(2, descuento=0.05)
        ok(f"Sala 2h  (IVA 19%, desc 10%) → ${c_sala:>12,.0f} COP")
        ok(f"Equipo 3d (IVA 19%)          → ${c_equipo:>12,.0f} COP")
        ok(f"Asesoría 2s (desc 5%)        → ${c_aseso:>12,.0f} COP")
    except Exception as e:
        err(f"Error: {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP 10: Cancelar reserva e intentar cancelarla de nuevo
    # ------------------------------------------------------------------
    sep("OP 10: Cancelar reserva y reintentar (debe fallar)")
    try:
        duver    = Cliente("Duver", 203634, 3102314466, "Duitama")
        reserva2 = Reserva(duver, equipo1, 2)
        reserva2.cancelar()
        ok(f"Reserva cancelada → Estado: {reserva2.estado}")
    except Exception as e:
        err(f"Error inesperado: {e}")

    print()
    try:
        reserva2.cancelar()
        err("Debió lanzar excepción")
    except ReservaError as e:
        ok(f"Excepción capturada → {e}")
        registrar_error(str(e))

    # ------------------------------------------------------------------
    # OP EXTRA: Servicio marcado como no disponible
    # ------------------------------------------------------------------
    sep("OP EXTRA: Servicio no disponible")
    try:
        equipo1.disponible = False
        cristian = Cliente("Cristian", 678901, 3206576540, "Mosquera")
        r_extra  = Reserva(cristian, equipo1, 1)
        r_extra.confirmar()
        err("Debió lanzar excepción")
    except ReservaError as e:
        ok(f"Excepción capturada → {e}")
        registrar_error(str(e))
    finally:
        equipo1.disponible = True  # Reactivar en finally

    # ------------------------------------------------------------------
    # RESUMEN
    # ------------------------------------------------------------------
    sep("RESUMEN FINAL")
    print(f"  Clientes activos: {diego}, {paola}, {duver}")
    print(f"  Servicios: {sala_a} | {equipo1} | {asesoria1}")
    print(f"  Reservas procesadas: {reserva1.estado}, {reserva2.estado}")
    print(f"\n  Todos los eventos registrados en: errores.log")
    sep()

    registrar_info("FIN DEL SISTEMA SOFTWARE FJ")
    registrar_info("="*40)
    print("\n  Sistema ejecutado sin interrupciones. ✅")
