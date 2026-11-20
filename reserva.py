# Importamos la clase abstracta, excepciones y registrador de logs del Compañero 1
from base_y_logs import (
    EntidadSistema, ErrorValidacionDatos, ReservaInvalidaError, 
    ErrorSistemaFJ, registrar_log
)
# Importamos la clase Cliente del Compañero 2 y Servicio del "Compañero 3"
from cliente import Cliente
from servicios import Servicio