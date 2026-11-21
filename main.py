# Importacion de los modulos creados por todo el equipo
from base_y_logs import ErrorSistemaFJ, registrar_log
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva


def ejecutar_simulacion():
    """Ejecuta la simulacion integral y controla los errores esperados."""
    print("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    registrar_log("=== INICIO DE SIMULACION DEL SISTEMA ===", "INFO")

    clientes = []
    servicios = []
    reservas = []

    # OPERACION 1: Registro valido de Cliente 1
    try:
        c1 = Cliente("CLI-01", "Laura Gomez", "1098765432", "laura.gomez@correo.com")
        clientes.append(c1)
        print("[OK] Op 1:", c1.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 1:", e)

    # OPERACION 2: Registro valido de Cliente 2
    try:
        c2 = Cliente("CLI-02", "Carlos Ruiz", "1045678901", "carlos.ruiz@empresa.co")
        clientes.append(c2)
        print("[OK] Op 2:", c2.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 2:", e)

    # OPERACION 3: Registro INVALIDO de Cliente (Correo con formato incorrecto)
    try:
        c_malo = Cliente("CLI-03", "Pedro Perez", "98765432", "pedro_sin_arroba.com")
        clientes.append(c_malo)
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 3 (Correo invalido):", e)

    # OPERACION 4: Registro INVALIDO de Cliente (Documento duplicado)
    try:
        c_duplicado = Cliente("CLI-04", "Laura Clon", "1098765432", "otro@correo.com")
        clientes.append(c_duplicado)
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 4 (Documento duplicado):", e)

    # OPERACION 5: Creacion polimorfica de servicios
    try:
        s1 = ReservaSala(
            "SRV-01", "Sala Juntas Norte", 80000, capacidad=12, disponible=True
        )
        s2 = AlquilerEquipo(
            "SRV-02", "Servidor Dell PowerEdge", 50000, "Servidores", disponible=True
        )
        s3 = AsesoriaEspecializada(
            "SRV-03", "Arquitectura Cloud", 120000, "DevOps", disponible=False
        )
        servicios.extend([s1, s2, s3])
        print("[OK] Op 5: 3 servicios creados correctamente.")
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 5:", e)

    # OPERACION 6: Registro invalido de servicio
    try:
        s_malo = AlquilerEquipo("SRV-04", "Portatil HP", -25000, "Computo")
        servicios.append(s_malo)
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 6 (Tarifa negativa):", e)

    # OPERACION 7: Reserva valida con descuento
    try:
        r1 = Reserva("RES-01", clientes[0], servicios[0], horas=3)
        r1.procesar_y_confirmar(descuento=10)
        reservas.append(r1)
        print("[OK] Op 7:", r1.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 7:", e)

    # OPERACION 8: Reserva valida adicional
    try:
        r2 = Reserva("RES-02", clientes[1], servicios[1], horas=6)
        r2.procesar_y_confirmar()
        reservas.append(r2)
        print("[OK] Op 8:", r2.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 8:", e)

    # OPERACION 9: Servicio inactivo
    try:
        r3 = Reserva("RES-03", clientes[0], servicios[2], horas=2)
        r3.procesar_y_confirmar()
    except ErrorSistemaFJ as e:
        print(
            f"[ERROR CONTROLADO] Op 9 (Servicio inactivo): {e} | Causa raiz: {e.__cause__}"
        )

    # OPERACION 10: Horas negativas
    try:
        r4 = Reserva("RES-04", clientes[1], servicios[0], horas=-4)
        r4.procesar_y_confirmar()
    except ErrorSistemaFJ as e:
        print(
            f"[ERROR CONTROLADO] Op 10 (Horas negativas): {e} | Causa raiz: {e.__cause__}"
        )

    # OPERACION 11: Cancelacion valida de una reserva confirmada
    try:
        r1.cancelar()
        reservas.append(r1)
        print("[OK] Op 11:", r1.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 11 (Cancelacion):", e)

    # OPERACION 12: Descuento fuera del rango permitido
    try:
        r5 = Reserva("RES-05", clientes[0], servicios[0], horas=2)
        r5.procesar_y_confirmar(descuento=150)
    except ErrorSistemaFJ as e:
        print(
            f"[ERROR CONTROLADO] Op 12 (Descuento invalido): {e} | Causa raiz: {e.__cause__}"
        )

    print("\n=== SIMULACION FINALIZADA EXITOSAMENTE SIN CAIDAS DEL SISTEMA ===")
    print("Verifica el archivo 'registro_eventos.log' generado en el directorio.")


if __name__ == "__main__":
    ejecutar_simulacion()
