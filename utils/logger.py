"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Permite identificar y clasificar errores de negocio y validación.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base de la cual heredan todos los errores del sistema."""

    def __init__(self, mensaje: str, codigo: str = "ERR-000"):
        # Almacenamos un código de error para facilitar la trazabilidad en los logs
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class ErrorValidacionDatos(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados tienen formato inválido o están vacíos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-VAL-01")


class ErrorClienteDuplicado(ErrorSistemaFJ):
    """Se lanza al intentar registrar un cliente con un documento ya existente."""

    def __init__(self, documento: str):
        super().__init__(
            f"El cliente con documento '{documento}' ya se encuentra registrado.",
            codigo="ERR-CLI-02",
        )


class ErrorServicioNoDisponible(ErrorSistemaFJ):
    """Se lanza cuando un servicio no existe, está inactivo o no cumple capacidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-SRV-03")


class ErrorReservaInvalida(ErrorSistemaFJ):
    """Se lanza cuando una reserva viola reglas de negocio (duración, estado, etc.)."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-RES-04")
