# Importamos la clase abstracta, excepciones y registrador de logs del Compañero 1
from base_y_logs import (
    EntidadSistema,
    ErrorValidacionDatos,
    ReservaInvalidaError,
    ErrorSistemaFJ,
    registrar_log,
)

# Importamos la clase Cliente del Compañero 2 y Servicio del "Compañero 3"
from cliente import Cliente
from servicios import Servicio


class Reserva(EntidadSistema):
    """
    Clase que representa una reserva en el sistema Software FJ,
    vinculando un Cliente con un Servicio determinado.
    """

    def __init__(
        self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: float
    ):
        # Llamamos al constructor de la clase base EntidadSistema
        super().__init__(id_reserva)

        # Validamos que los objetos recibidos sean instancias válidas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Se requiere una instancia válida de la clase Cliente."
            )
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Se requiere una instancia válida de la clase Servicio."
            )

        # Asignación de atributos
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0
