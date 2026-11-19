"""
Módulo que define la clase abstracta general del dominio.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """
    Clase abstracta general que provee atributos comunes de auditoría
    y obliga a las subclases a implementar su representación y validación.
    """

    def __init__(self, id_entidad: str):
        # Atributo protegido para el identificador único en memoria
        self._id = id_entidad
        # Fecha y hora exacta de creación del objeto
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que cada entidad debe implementar para describirse."""
        pass
