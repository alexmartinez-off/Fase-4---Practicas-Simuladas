# Importa el módulo base con clase abstracta, excepciones y función de registro de logs
try:
    # Intenta importar los componentes definidos en base_y_logs.py
    from base_y_logs import (
        EntidadSistema,  # Clase abstracta general del sistema
        ErrorValidacion,  # Excepción personalizada para errores de validación
        registrar_log,  # Función para guardar eventos y errores en archivo de logs
    )
except ImportError:
    # Importa ABC y abstractmethod para definir clase abstracta de respaldo si falta en base_y_logs.py
    from abc import ABC, abstractmethod
    # Importa datetime para generar marcas de fecha y hora
    from datetime import datetime

    # Excepción personalizada de respaldo para errores de validación
    class ErrorValidacion(Exception):
        """Excepción lanzada cuando los datos de una entidad o validación son inválidos."""
        pass  # Sin cuerpo adicional al heredar de Exception

    # Clase abstracta de respaldo con ID y fecha de registro
    class EntidadSistema(ABC):
        """Clase abstracta general con identificador único y fecha de registro."""

        def __init__(self, entidad_id):  # Recibe el identificador de la entidad
            self.id = entidad_id  # Asigna el ID público
            self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Guarda fecha y hora

        @abstractmethod  # Obliga a las subclases a implementar este método
        def describir(self):
            """Retorna una descripción de la entidad."""
            pass  # Implementado en clases hijas

    # Función de respaldo para registrar eventos y errores en registro_eventos.log
    def registrar_log(mensaje):
        """Registra un mensaje de evento o error en el archivo de texto registro_eventos.log."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene fecha y hora actual
        with open("registro_eventos.log", "a", encoding="utf-8") as archivo_log:  # Abre o crea el log
            archivo_log.write(f"[{marca_tiempo}] {mensaje}\n")  # Escribe el evento o error con hora


class Cliente(EntidadSistema):
    """Representa un cliente con atributos encapsulados, validaciones y registro en logs."""

    def __init__(self, id, nombre, documento, correo):  # Inicializa un cliente con sus datos
        """Crea una instancia validada de Cliente y registra el resultado en el log."""
        super().__init__(id)  # Inicializa id y fecha_registro desde EntidadSistema
        self._nombre = None  # Atributo encapsulado para el nombre
        self._documento = None  # Atributo encapsulado para el documento
        self._correo = None  # Atributo encapsulado para el correo

        try:  # Valida y asigna los datos mediante las propiedades con setters
            self.nombre = nombre  # Valida y guarda el nombre
            self.documento = documento  # Valida y guarda el documento
            self.correo = correo  # Valida y guarda el correo
        except ErrorValidacion as exc:  # Captura fallos de validación
            registrar_log(f"ERROR | Cliente ID={id} | Fallo al crear cliente: {exc}")  # Registra el error
            raise  # Relanza la excepción para que el programa principal la controle
        else:  # Se ejecuta si todas las validaciones fueron correctas
            registrar_log(  # Registra la creación exitosa del cliente
                f"INFO | Cliente creado correctamente | ID={self.id}, Nombre={self._nombre}, "
                f"Documento={self._documento}, Correo={self._correo}"
            )

    @property  # Getter para leer el nombre encapsulado
    def nombre(self):
        """Obtiene el nombre del cliente."""
        return self._nombre  # Retorna _nombre

    @nombre.setter  # Setter con validación para nombre
    def nombre(self, valor):
        """Valida que el nombre no esté vacío y asigna el valor encapsulado."""
        try:  # Revisa que el nombre sea texto no vacío
            if valor is None or not isinstance(valor, str):  # Verifica tipo string
                raise ErrorValidacion("El nombre del cliente debe ser un texto válido.")  # Error si no es texto
            nombre_limpio = valor.strip()  # Quita espacios en los extremos
            if not nombre_limpio:  # Revisa que no quede vacío
                raise ErrorValidacion("El nombre del cliente no puede estar vacío.")  # Error si está vacío
        except ErrorValidacion:  # Captura error de validación
            raise  # Propaga la excepción
        else:  # Si es válido
            self._nombre = nombre_limpio  # Guarda en _nombre

    @property  # Getter para leer el documento encapsulado
    def documento(self):
        """Obtiene el documento del cliente."""
        return self._documento  # Retorna _documento

    @documento.setter  # Setter con validación para documento
    def documento(self, valor):
        """Valida que el documento sea válido y no esté vacío."""
        try:  # Valida formato y longitud mínima del documento
            if valor is None:  # Verifica que no sea None
                raise ErrorValidacion("El documento del cliente no puede estar vacío.")  # Error si falta dato
            documento_texto = str(valor).strip()  # Convierte a texto y limpia espacios
            if not documento_texto or not documento_texto.isalnum() or len(documento_texto) < 5:  # Revisa formato
                raise ErrorValidacion(  # Lanza error si no cumple
                    f"Documento inválido ('{valor}'): debe tener al menos 5 caracteres alfanuméricos."
                )
        except ErrorValidacion:  # Captura error de validación
            raise  # Propaga la excepción
        else:  # Si es válido
            self._documento = documento_texto  # Guarda en _documento

    @property  # Getter para leer el correo encapsulado
    def correo(self):
        """Obtiene el correo electrónico del cliente."""
        return self._correo  # Retorna _correo

    @correo.setter  # Setter con validación para correo
    def correo(self, valor):
        """Valida que el correo no esté vacío y contenga '@' y dominio válido."""
        try:  # Valida estructura básica del correo
            if valor is None or not isinstance(valor, str):  # Verifica tipo string
                raise ErrorValidacion("El correo electrónico debe ser un texto válido.")  # Error si no es texto
            correo_limpio = valor.strip()  # Limpia espacios en los extremos
            if not correo_limpio:  # Verifica que no esté vacío
                raise ErrorValidacion("El correo electrónico no puede estar vacío.")  # Error si está vacío
            if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:  # Exige '@' y dominio con punto
                raise ErrorValidacion(f"Correo electrónico inválido ('{correo_limpio}'): debe contener '@' y dominio.")  # Error
        except ErrorValidacion:  # Captura error de validación
            raise  # Propaga la excepción
        else:  # Si es válido
            self._correo = correo_limpio  # Guarda en _correo

    def describir(self):  # Implementa el método abstracto de EntidadSistema
        """Devuelve una descripción legible del cliente."""
        return f"Cliente [ID: {self.id}] - Nombre: {self._nombre} | Doc: {self._documento} | Correo: {self._correo}"  # Formato legible
