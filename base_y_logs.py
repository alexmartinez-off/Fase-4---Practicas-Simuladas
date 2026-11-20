"""
Modulo base_y_logs.py - Sistema Integral de Gestion Software FJ.
Contiene:
1. La clase abstracta general EntidadSistema.
2. La jerarquia de excepciones personalizadas.
3. El sistema de registro de eventos y errores en 'registro_eventos.log'.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os


# ==============================================================================
# 1. EXCEPCIONES PERSONALIZADAS
# ==============================================================================

class ErrorSistemaFJ(Exception):
    """Excepcion base de la cual heredan todos los errores del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR-000"):
        # Codigo interno para facilitar la trazabilidad en el archivo de logs
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class ErrorValidacion(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados estan vacios o tienen formato invalido."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-VAL-01")


class ErrorClienteDuplicado(ErrorSistemaFJ):
    """Se lanza al intentar registrar un cliente con un documento ya existente."""

    def __init__(self, documento: str):
        super().__init__(
            f"El cliente con documento '{documento}' ya se encuentra registrado.",
            codigo="ERR-CLI-02",
        )


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio no existe, esta inactivo o no tiene cupo."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-SRV-03")


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva incumple reglas de negocio (horas, estado, etc.)."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-RES-04")


# ==============================================================================
# 2. SISTEMA DE LOGS EN ARCHIVO (SIN BASES DE DATOS)
# ==============================================================================

def _configurar_logger() -> logging.Logger:
    """Configura el logger que escribe en el archivo 'registro_eventos.log'."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitamos duplicar manejadores si el modulo se importa varias veces
    if not logger.handlers:
        # Archivo de texto plano en la raiz tal como exige la guia y el equipo
        file_handler = logging.FileHandler(
            "registro_eventos.log", mode="a", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        # Salida tambien por consola para visualizar las simulaciones en ejecucion
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formato)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Instancia global del logger lista para usar
_logger_sistema = _configurar_logger()


def registrar_log(mensaje: str, nivel: str = "INFO") -> None:
    """
    Registra un evento o error en el archivo 'registro_eventos.log'.
    :param mensaje: Descripcion del evento o error ocurrido.
    :param nivel: Nivel de severidad ('INFO', 'ERROR', 'WARNING', 'DEBUG').
    """
    # Permite llamadas historicas con formato (nivel, mensaje) y el formato
    # establecido por el resto del proyecto (mensaje, nivel).
    niveles_validos = {"INFO", "ERROR", "WARNING", "DEBUG"}
    if str(mensaje).upper().strip() in niveles_validos and str(nivel).upper().strip() not in niveles_validos:
        mensaje, nivel = nivel, mensaje

    nivel_normalizado = nivel.upper().strip()
    if nivel_normalizado == "ERROR":
        _logger_sistema.error(mensaje)
    elif nivel_normalizado == "WARNING":
        _logger_sistema.warning(mensaje)
    elif nivel_normalizado == "DEBUG":
        _logger_sistema.debug(mensaje)
    else:
        _logger_sistema.info(mensaje)


# ==============================================================================
# 3. CLASE ABSTRACTA GENERAL
# ==============================================================================

class EntidadSistema(ABC):
    """
    Clase abstracta general de la que heredan Cliente, Servicio y Reserva.
    Garantiza atributos comunes de identificacion y fecha de registro.
    """

    def __init__(self, id_entidad: str):
        # Validamos que el ID no llegue vacio
        if not id_entidad or not str(id_entidad).strip():
            raise ErrorValidacion("El identificador de la entidad no puede estar vacio.")

        # Atributos protegidos accesibles para las clases hijas
        self._id = str(id_entidad).strip()
        self._fecha_registro = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador unico de la entidad."""
        return self._id

    @property
    def fecha_registro(self) -> datetime:
        """Retorna la fecha y hora exacta en que se creo el registro."""
        return self._fecha_registro

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Metodo abstracto obligatorio para que cada entidad describa su estado."""
        pass
