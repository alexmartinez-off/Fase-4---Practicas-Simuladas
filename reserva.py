# Importamos la clase abstracta, excepciones y registrador de logs del Companero 1
from base_y_logs import (
    EntidadSistema,
    ReservaInvalidaError,
    ErrorSistemaFJ,
    registrar_log,
)

# Importamos la clase Cliente del Companero 2 y Servicio del "Companero 3"
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

        # Validamos que los objetos recibidos sean instancias validas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Se requiere una instancia valida de la clase Cliente."
            )
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Se requiere una instancia valida de la clase Servicio."
            )

        # Asignacion de atributos
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0


    def procesar_y_confirmar(self, descuento: float = 0.0):
        """
        Calcula el costo total invocando el polimorfismo del servicio
        y confirma la reserva con manejo estricto de excepciones.
        """
        try:
            if self.estado == "CANCELADA":
                raise ReservaInvalidaError(
                    "No se puede confirmar una reserva previamente cancelada."
                )

            # Delegacion polimorfica del calculo de tarifa segun el servicio asignado
            self.costo_total = self.servicio.calcular_costo(
                self.horas, descuento=descuento
            )
            self.estado = "CONFIRMADA"
            registrar_log(
                "INFO",
                f"Reserva {self.id} CONFIRMADA para {self.cliente.nombre}. "
                f"Total: ${self.costo_total}",
            )

        except ErrorSistemaFJ as error_origen:
            # Encadenamiento de excepciones: captura el error original y relanza ReservaInvalidaError
            self.estado = "FALLIDA"
            registrar_log("ERROR", f"Error procesando reserva {self.id}: {error_origen}")
            raise ReservaInvalidaError(
                f"Fallo al procesar la reserva {self.id}"
            ) from error_origen

        finally:
            # El bloque finally garantiza el registro de auditoria sin importar si hubo error o exito
            registrar_log(
                "INFO",
                f"Auditoria Reserva {self.id} -> Estado actual final: {self.estado}",
            )

    def cancelar(self):
        """Cancela una reserva activa y actualiza su estado."""
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError(
                f"La reserva {self.id} ya se encuentra cancelada."
            )
        self.estado = "CANCELADA"
        registrar_log("INFO", f"Reserva {self.id} CANCELADA por el usuario.")

    def obtener_resumen(self) -> str:
        """Implementacion del metodo abstracto heredado de EntidadSistema."""
        return (
            f"Reserva [{self.id}] | Estado: {self.estado} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.obtener_resumen()} | Total: ${self.costo_total}"
        )
