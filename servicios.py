"""Modulo de servicios para el proyecto Software FJ (Fase 4).

Responsable: Companero 3 - rama 'servicios'.

Este archivo define la clase abstracta Servicio y tres implementaciones:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

Contrato de integracion acordado por el equipo:
    calcular_costo(horas, descuento=0, impuesto=0)
    describir_servicio()

Los porcentajes de descuento e impuesto se expresan como numeros de 0 a 100.
El metodo calcular_costo devuelve el valor total como float, redondeado a
2 decimales. Los datos se gestionan en memoria (sin base de datos).
"""

from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Las excepciones y el registro centralizado pertenecen al Companero 1.
from base_y_logs import ErrorValidacion, ServicioNoDisponibleError, registrar_log


# Constante de redondeo a dos cifras decimales (moneda).
DOS_DECIMALES = Decimal("0.01")


def _registrar_error(mensaje):
    """Registra un error sin ocultar la excepcion que lo origino."""
    registrar_log(f"ERROR SERVICIOS: {mensaje}")


def _validar_texto(valor, campo):
    """Comprueba que el campo contenga texto y no este vacio."""
    if not isinstance(valor, str) or not valor.strip():
        mensaje = f"{campo} debe ser un texto no vacio."
        _registrar_error(mensaje)
        raise ErrorValidacion(mensaje)
    return valor.strip()


def _a_decimal(valor, campo, *, minimo=Decimal("0"), incluir_minimo=True):
    """Convierte un numero a Decimal y rechaza valores no validos."""
    if isinstance(valor, bool):
        mensaje = f"{campo} debe ser numerico, no booleano."
        _registrar_error(mensaje)
        raise ErrorValidacion(mensaje)

    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as error:
        mensaje = f"{campo} debe ser un numero valido."
        _registrar_error(mensaje)
        raise ErrorValidacion(mensaje) from error

    if not numero.is_finite():
        mensaje = f"{campo} debe ser un numero finito."
        _registrar_error(mensaje)
        raise ErrorValidacion(mensaje)

    cumple_minimo = numero >= minimo if incluir_minimo else numero > minimo
    if not cumple_minimo:
        comparacion = "mayor o igual que" if incluir_minimo else "mayor que"
        mensaje = f"{campo} debe ser {comparacion} {minimo}."
        _registrar_error(mensaje)
        raise ErrorValidacion(mensaje)
    return numero


def _validar_porcentaje(valor, campo):
    """Verifica que descuento o impuesto esten entre 0 % y 100 %."""
    porcentaje = _a_decimal(valor, campo)
    if porcentaje > Decimal("100"):
        mensaje = f"{campo} no puede superar el 100 %."
        _registrar_error(mensaje)
        raise ErrorValidacion(mensaje)
    return porcentaje


class Servicio(ABC):
    """Clase abstracta con atributos encapsulados y operaciones comunes."""

    def __init__(self, id, nombre, tarifa_hora, disponible=True):
        # La identificacion permite localizar el servicio en listas internas.
        self.__id = _validar_texto(str(id), "El ID")
        self.__nombre = _validar_texto(nombre, "El nombre")
        self.__tarifa_hora = _a_decimal(tarifa_hora, "La tarifa por hora", incluir_minimo=False)
        if not isinstance(disponible, bool):
            mensaje = "La disponibilidad debe ser True o False."
            _registrar_error(mensaje)
            raise ErrorValidacion(mensaje)
        self.__disponible = disponible

    @property
    def id(self):
        """Retorna la identificacion del servicio."""
        return self.__id

    @property
    def nombre(self):
        """Retorna el nombre publico del servicio."""
        return self.__nombre

    @property
    def tarifa_hora(self):
        """Retorna la tarifa en formato numerico."""
        return float(self.__tarifa_hora)

    @property
    def disponible(self):
        """Indica si se pueden solicitar nuevas reservas."""
        return self.__disponible

    def cambiar_disponibilidad(self, disponible):
        """Habilita o deshabilita el servicio de forma controlada."""
        if not isinstance(disponible, bool):
            mensaje = "La disponibilidad debe ser True o False."
            _registrar_error(mensaje)
            raise ErrorValidacion(mensaje)
        self.__disponible = disponible
        registrar_log(f"EVENTO: Disponibilidad de {self.__id} cambiada a {disponible}.")

    def _calcular_total(self, horas, descuento=0, impuesto=0, *, recargo=0):
        """Valida los datos y aplica descuento e impuesto al costo base.

        El recargo adicional es un monto fijo por operacion, si procede.
        """
        if not self.__disponible:
            mensaje = f"El servicio {self.__nombre} no esta disponible."
            _registrar_error(mensaje)
            raise ServicioNoDisponibleError(mensaje)

        duracion = _a_decimal(horas, "Las horas", incluir_minimo=False)
        descuento_val = _validar_porcentaje(descuento, "El descuento")
        impuesto_val = _validar_porcentaje(impuesto, "El impuesto")
        recargo_val = _a_decimal(recargo, "El recargo")

        # Primero se aplica el descuento; despues, el impuesto.
        subtotal = self.__tarifa_hora * duracion + recargo_val
        con_descuento = subtotal * (Decimal("1") - descuento_val / Decimal("100"))
        total = con_descuento * (Decimal("1") + impuesto_val / Decimal("100"))
        total = total.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)
        registrar_log(f"EVENTO: Costo calculado de {self.__id}: {total}.")
        return float(total)

    @abstractmethod
    def calcular_costo(self, horas, descuento=0, impuesto=0):
        """Calcula el costo del servicio (implementado en cada clase hija)."""

    @abstractmethod
    def describir_servicio(self):
        """Devuelve la descripcion propia de cada tipo de servicio."""

    def obtener_resumen(self):
        """Proporciona el resumen publico esperado por las reservas."""
        return self.describir_servicio()

    @abstractmethod
    def validar_parametros(self):
        """Comprueba los atributos especializados de cada servicio."""


class ReservaSala(Servicio):
    """Servicio de reserva de salas con capacidad maxima definida."""

    def __init__(self, id, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(id, nombre, tarifa_hora, disponible)
        self.__capacidad = capacidad
        self.validar_parametros()
        registrar_log(f"EVENTO: Sala registrada: {self.id}.")

    def validar_parametros(self):
        """La capacidad debe ser un entero positivo."""
        if type(self.__capacidad) is not int or self.__capacidad <= 0:
            mensaje = "La capacidad de la sala debe ser un entero positivo."
            _registrar_error(mensaje)
            raise ErrorValidacion(mensaje)
        return True

    def calcular_costo(self, horas, descuento=0, impuesto=0):
        """Aplica la tarifa de la sala por el numero de horas."""
        self.validar_parametros()
        return self._calcular_total(horas, descuento, impuesto)

    def describir_servicio(self):
        """Muestra datos de la sala y su capacidad."""
        return (f"Reserva de sala: {self.nombre} | ID: {self.id} | "
                f"Capacidad: {self.__capacidad} personas | "
                f"Tarifa: ${self.tarifa_hora:.2f}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnologicos."""

    def __init__(self, id, nombre, tarifa_hora, tipo_equipo, disponible=True):
        super().__init__(id, nombre, tarifa_hora, disponible)
        self.__tipo_equipo = tipo_equipo
        self.validar_parametros()
        registrar_log(f"EVENTO: Equipo registrado: {self.id}.")

    def validar_parametros(self):
        """El tipo de equipo debe estar diligenciado."""
        self.__tipo_equipo = _validar_texto(self.__tipo_equipo, "El tipo de equipo")
        return True

    def calcular_costo(self, horas, descuento=0, impuesto=0):
        """Calcula el alquiler con base en la tarifa y la duracion."""
        self.validar_parametros()
        return self._calcular_total(horas, descuento, impuesto)

    def describir_servicio(self):
        """Muestra el equipo disponible para alquilar."""
        return (f"Alquiler de equipo: {self.nombre} | ID: {self.id} | "
                f"Tipo: {self.__tipo_equipo} | "
                f"Tarifa: ${self.tarifa_hora:.2f}/hora")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria tecnica o profesional por horas."""

    def __init__(self, id, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(id, nombre, tarifa_hora, disponible)
        self.__especialidad = especialidad
        self.validar_parametros()
        registrar_log(f"EVENTO: Asesoria registrada: {self.id}.")

    def validar_parametros(self):
        """La especialidad de la asesoria no puede estar vacia."""
        self.__especialidad = _validar_texto(self.__especialidad, "La especialidad")
        return True

    def calcular_costo(self, horas, descuento=0, impuesto=0):
        """Calcula el costo de una asesoria segun las horas solicitadas."""
        self.validar_parametros()
        return self._calcular_total(horas, descuento, impuesto)

    def describir_servicio(self):
        """Describe el area de especializacion del asesor."""
        return (f"Asesoria especializada: {self.nombre} | ID: {self.id} | "
                f"Especialidad: {self.__especialidad} | "
                f"Tarifa: ${self.tarifa_hora:.2f}/hora")
