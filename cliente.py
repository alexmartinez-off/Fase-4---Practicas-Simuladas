# Importamos las clases y funciones base que ya creó nuestro compañero en base_y_logs.py
from base_y_logs import EntidadSistema, ErrorValidacion, registrar_log


class Cliente(EntidadSistema):
    # Clase para manejar los clientes de Software FJ heredando id y fecha de EntidadSistema
    def __init__(self, id, nombre, documento, correo):
        # Llamamos al constructor padre para validar el id y guardar la fecha de registro
        super().__init__(id)
        # Guardamos los datos en atributos privados para protegerlos (encapsulación)
        self.__nombre = None
        self.__documento = None
        self.__correo = None

        # Intentamos asignar y validar cada dato del cliente
        try:
            # Pasamos por las propiedades para que se ejecuten las validaciones
            self.nombre = nombre
            self.documento = documento
            self.correo = correo
        except ErrorValidacion as err:
            # Si algo falla en la validación, lo dejamos anotado en el archivo de logs
            registrar_log(f"Fallo creando cliente ({id}): {err}", "ERROR")
            # Volvemos a lanzar el error para que el programa principal decida cómo seguir
            raise
        else:
            # Solo se ejecuta si nombre, documento y correo pasaron todas las reglas
            registrar_log(f"Cliente registrado: {self.__nombre} (Doc: {self.__documento})", "INFO")

    @property
    def nombre(self):
        # Devuelve el nombre guardado de forma privada
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Validamos que el nombre exista, sea texto y no quede vacío tras quitar espacios
        try:
            if not isinstance(valor, str) or not valor.strip():
                # Lanzamos la excepción personalizada si el nombre no es válido
                raise ErrorValidacion("El nombre no puede estar vacío.")
        except ErrorValidacion:
            # Propagamos el error hacia arriba
            raise
        else:
            # Guardamos el nombre limpio sin espacios extra a los lados
            self.__nombre = valor.strip()

    @property
    def documento(self):
        # Devuelve el documento guardado de forma privada
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # Revisamos que el documento no venga vacío
        try:
            if valor is None:
                raise ErrorValidacion("El documento es obligatorio.")
            # Convertimos a texto y quitamos espacios sobrantes
            doc = str(valor).strip()
            # Pedimos al menos 5 caracteres y que solo tenga letras o números
            if len(doc) < 5 or not doc.isalnum():
                raise ErrorValidacion("El documento debe tener mínimo 5 caracteres alfanuméricos.")
        except ErrorValidacion:
            raise
        else:
            # Guardamos el documento ya revisado
            self.__documento = doc

    @property
    def correo(self):
        # Devuelve el correo guardado de forma privada
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Revisamos que el correo tenga un formato básico válido con '@' y punto
        try:
            if not isinstance(valor, str) or not valor.strip():
                raise ErrorValidacion("El correo no puede estar vacío.")
            correo_limpio = valor.strip()
            # Verificamos que tenga '@' y un dominio con punto después del '@'
            if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:
                raise ErrorValidacion("El correo debe tener un formato válido (ejemplo: usuario@correo.com).")
        except ErrorValidacion:
            raise
        else:
            # Guardamos el correo limpio
            self.__correo = correo_limpio

    def obtener_resumen(self):
        # Implementamos el método abstracto de EntidadSistema para mostrar los datos del cliente
        return (
            f"Cliente ID: {self.id} | Nombre: {self.__nombre} | "
            f"Documento: {self.__documento} | Correo: {self.__correo}"
        )
