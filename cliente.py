# Importa el módulo de utilidades base, clase abstracta, excepciones y registro de logs[cite: 11]
try:
    # Intenta importar los componentes esperados desde base_y_logs.py[cite: 11]
    from base_y_logs import (  # Importa los elementos base definidos por el equipo[cite: 11]
        EntidadSistema,  # Clase abstracta base para entidades del sistema[cite: 11]
        ErrorValidacion,  # Excepción personalizada para errores de validación[cite: 11]
        registrar_log,  # Función encargada de guardar eventos y errores en el archivo de logs[cite: 11]
    )
except ImportError:
    # Importa ABC y abstractmethod para definir la clase abstracta de respaldo si hace falta[cite: 11]
    from abc import ABC, abstractmethod
    # Importa datetime para asignar la fecha de registro en el respaldo[cite: 11]
    from datetime import datetime

    # Define una excepción personalizada de respaldo si no existe en base_y_logs.py[cite: 11]
    class ErrorValidacion(Exception):
        """Excepción lanzada cuando los datos de una entidad o validación son inválidos."""
        pass  # No requiere cuerpo adicional más allá de heredar de Exception

    # Define una clase abstracta de respaldo si no existe en base_y_logs.py[cite: 11]
    class EntidadSistema(ABC):
        """Clase abstracta general con identificador único y fecha de registro."""

        def __init__(self, entidad_id):  # Constructor que recibe el identificador de la entidad
            self.id = entidad_id  # Asigna el atributo público id
            self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Guarda la fecha y hora actual

        @abstractmethod  # Marca el método como obligatorio para las subclases
        def describir(self):
            """Retorna una descripción de la entidad."""
            pass  # Será implementado en las clases hijas

    # Define una función de respaldo para escribir en registro_eventos.log sin base de datos[cite: 11]
    def registrar_log(mensaje):
        """Registra un mensaje de evento o error en el archivo de texto registro_eventos.log."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene fecha y hora actual
        with open("registro_eventos.log", "a", encoding="utf-8") as archivo_log:  # Abre o crea el log en modo append
            archivo_log.write(f"[{marca_tiempo}] {mensaje}\n")  # Escribe la línea con marca de tiempo y salto de línea


class Cliente(EntidadSistema):
    """Representa un cliente del sistema con datos encapsulados, validaciones y registro en logs."""[cite: 11]

    def __init__(self, id, nombre, documento, correo):  # Inicializa un cliente con sus datos obligatorios[cite: 11]
        """Crea una instancia validada de Cliente y registra el evento o error correspondiente."""
        super().__init__(id)  # Invoca el constructor de la clase padre EntidadSistema para asignar id y fecha[cite: 11]
        self._nombre = None  # Inicializa el atributo encapsulado para el nombre completo[cite: 11]
        self._documento = None  # Inicializa el atributo encapsulado para el número de documento[cite: 11]
        self._correo = None  # Inicializa el atributo encapsulado para el correo electrónico[cite: 11]

        try:  # Inicia bloque try para validar y asignar los datos del cliente[cite: 11]
            self.nombre = nombre  # Usa el setter de nombre para validar y guardar[cite: 11]
            self.documento = documento  # Usa el setter de documento para validar y guardar[cite: 11]
            self.correo = correo  # Usa el setter de correo para validar y guardar[cite: 11]
        except ErrorValidacion as exc:  # Captura errores de validación lanzados por los setters[cite: 11]
            registrar_log(f"ERROR | Cliente ID={id} | Fallo al crear cliente: {exc}")  # Registra el error en el archivo log[cite: 11]
            raise  # Relanza la excepción para que el llamador o main.py también la maneje[cite: 11]
        else:  # Se ejecuta únicamente si todas las validaciones pasaron sin excepciones[cite: 11]
            registrar_log(  # Registra un evento exitoso de creación de cliente[cite: 11]
                f"INFO | Cliente creado correctamente | ID={self.id}, Nombre={self._nombre}, "
                f"Documento={self._documento}, Correo={self._correo}"
            )

    @property  # Define un getter para acceder al nombre de forma controlada[cite: 11]
    def nombre(self):
        """Obtiene el nombre encapsulado del cliente."""
        return self._nombre  # Retorna el valor almacenado en _nombre

    @nombre.setter  # Define un setter con validación estricta para el nombre[cite: 11]
    def nombre(self, valor):
        """Valida que el nombre no esté vacío y asigna el valor encapsulado."""
        try:  # Intenta limpiar y validar el valor recibido[cite: 11]
            if valor is None or not isinstance(valor, str):  # Verifica que sea una cadena de texto[cite: 11]
                raise ErrorValidacion("El nombre del cliente debe ser un texto válido.")  # Lanza error si no es texto[cite: 11]
            nombre_limpio = valor.strip()  # Elimina espacios en blanco al inicio y al final
            if not nombre_limpio:  # Verifica que no quede vacío tras quitar espacios[cite: 11]
                raise ErrorValidacion("El nombre del cliente no puede estar vacío.")  # Lanza error si está vacío[cite: 11]
        except ErrorValidacion:  # Captura la excepción de validación[cite: 11]
            raise  # Propaga ErrorValidacion hacia arriba[cite: 11]
        else:  # Si pasa las comprobaciones sin errores[cite: 11]
            self._nombre = nombre_limpio  # Guarda el nombre validado en el atributo encapsulado[cite: 11]

    @property  # Define un getter para acceder al documento de identidad[cite: 11]
    def documento(self):
        """Obtiene el documento encapsulado del cliente."""
        return self._documento  # Retorna el valor almacenado en _documento

    @documento.setter  # Define un setter con validación para el documento[cite: 11]
    def documento(self, valor):
        """Valida que el documento sea válido y no esté vacío."""
        try:  # Intenta convertir y validar el documento[cite: 11]
            if valor is None:  # Comprueba que el documento no sea None[cite: 11]
                raise ErrorValidacion("El documento del cliente no puede estar vacío.")  # Lanza error si falta valor[cite: 11]
            documento_texto = str(valor).strip()  # Convierte a cadena y quita espacios sobrantes
            if not documento_texto or not documento_texto.isalnum() or len(documento_texto) < 5:  # Valida formato y longitud mínima[cite: 11]
                raise ErrorValidacion(  # Lanza excepción si el documento es inválido[cite: 11]
                    f"Documento inválido ('{valor}'): debe tener al menos 5 caracteres alfanuméricos."
                )
        except ErrorValidacion:  # Captura ErrorValidacion si ocurrió[cite: 11]
            raise  # Relanza la excepción[cite: 11]
        else:  # Si el documento es válido[cite: 11]
            self._documento = documento_texto  # Guarda el documento en el atributo encapsulado[cite: 11]

    @property  # Define un getter para acceder al correo electrónico[cite: 11]
    def correo(self):
        """Obtiene el correo electrónico encapsulado del cliente."""
        return self._correo  # Retorna el valor almacenado en _correo

    @correo.setter  # Define un setter con validación de formato básico para correo[cite: 11]
    def correo(self, valor):
        """Valida que el correo no esté vacío y contenga '@' y dominio válido."""
        try:  # Inicia validación del correo electrónico[cite: 11]
            if valor is None or not isinstance(valor, str):  # Verifica que el correo sea texto[cite: 11]
                raise ErrorValidacion("El correo electrónico debe ser un texto válido.")  # Lanza error si no es texto[cite: 11]
            correo_limpio = valor.strip()  # Elimina espacios alrededor del correo
            if not correo_limpio:  # Verifica que el campo no esté vacío[cite: 11]
                raise ErrorValidacion("El correo electrónico no puede estar vacío.")  # Lanza error si está vacío[cite: 11]
            if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:  # Exige '@' y punto en el dominio[cite: 11]
                raise ErrorValidacion(f"Correo electrónico inválido ('{correo_limpio}'): debe contener '@' y dominio.")  # Lanza error[cite: 11]
        except ErrorValidacion:  # Captura ErrorValidacion en caso de fallo[cite: 11]
            raise  # Propaga la excepción[cite: 11]
        else:  # Si el correo cumple las reglas[cite: 11]
            self._correo = correo_limpio  # Asigna el correo al atributo encapsulado[cite: 11]

    def describir(self):  # Implementa el método abstracto heredado de EntidadSistema[cite: 11]
        """Devuelve una descripción legible del cliente."""
        return f"Cliente [ID: {self.id}] - Nombre: {self._nombre} | Doc: {self._documento} | Correo: {self._correo}"  # Formatea datos
