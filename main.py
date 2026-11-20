# Importación de los módulos creados por todo el equipo
from base_y_logs import ErrorSistemaFJ, registrar_log
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva


def ejecutar_simulacion():
    """Ejecuta las pruebas obligatorias verificando la robustez del programa."""
    print("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    registrar_log("INFO", "=== INICIO DE SIMULACIÓN DEL SISTEMA ===")

    # Colecciones en memoria para almacenar entidades
    clientes = []
    servicios = []
    reservas = []

    # OPERACIÓN 1: Registro válido de Cliente 1
    try:
        c1 = Cliente("CLI-01", "Laura Gómez", "1098765432", "laura.gomez@correo.com")
        clientes.append(c1)
        print("[OK] Op 1:", c1.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 1:", e)

    # OPERACIÓN 2: Registro válido de Cliente 2
    try:
        c2 = Cliente("CLI-02", "Carlos Ruiz", "1045678901", "carlos.ruiz@empresa.co")
        clientes.append(c2)
        print("[OK] Op 2:", c2.obtener_resumen())
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 2:", e)

    # OPERACIÓN 3: Registro INVÁLIDO de Cliente (Correo con formato incorrecto)
    try:
        c_malo = Cliente("CLI-03", "Pedro Pérez", "98765432", "pedro_sin_arroba.com")
        clientes.append(c_malo)
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 3 (Correo inválido):", e)

    # OPERACIÓN 4: Registro INVÁLIDO de Cliente (Documento duplicado)
    try:
        c_duplicado = Cliente("CLI-04", "Laura Clon", "1098765432", "otro@correo.com")
        clientes.append(c_duplicado)
    except ErrorSistemaFJ as e:
        print("[ERROR CONTROLADO] Op 4 (Documento duplicado):", e)


if __name__ == "__main__":
    ejecutar_simulacion()
