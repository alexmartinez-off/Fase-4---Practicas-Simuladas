"""
Módulo encargado de configurar el sistema de logging.
Cumple la restricción de usar archivos exclusivamente para eventos y errores.
"""

import logging
import os


def configurar_logger() -> logging.Logger:
    """Configura y retorna el logger principal del sistema."""
    # Aseguramos que exista el directorio 'logs' antes de crear el archivo
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitamos duplicar handlers si la función se llama más de una vez
    if not logger.handlers:
        # Manejador para escribir en el archivo logs/sistema_fj.log con codificación UTF-8
        file_handler = logging.FileHandler("logs/sistema_fj.log", mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Manejador para mostrar mensajes en consola durante la simulación
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formato detallado con fecha, nivel de severidad y mensaje
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formato)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
