# Sistema Integral de Gestion de Clientes, Servicios y Reservas - Software FJ

## Descripcion del Proyecto

Este repositorio contiene el codigo fuente desarrollado para la Fase 4 (Practicas Simuladas) del curso de Programacion (Codigo 213023) de la Universidad Nacional Abierta y a Distancia (UNAD).

El proposito del proyecto es construir una aplicacion modular en Python para la empresa Software FJ que gestione clientes, servicios (reservas de salas, alquiler de equipos y asesorias especializadas) y reservas, aplicando los principios de la Programacion Orientada a Objetos (POO) y manejo avanzado de excepciones sin emplear bases de datos.

## Estructura del Repositorio y Modulos

El proyecto se dividio en modulos independientes desarrollados mediante ramas de trabajo en GitHub:

- `base_y_logs.py`: Define la clase abstracta general `EntidadSistema`, las excepciones personalizadas del sistema y la funcion de auditoria `registro_eventos.log`.
- `cliente.py`: Implementa la clase `Cliente` con encapsulacion de datos personales, validacion de formatos (documento, correo) y control de registros duplicados.
- `servicios.py`: Define la clase abstracta `Servicio` y las clases especializadas `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`, implementando polimorfismo en el calculo de tarifas.
- `reserva.py`: Gestiona la vinculacion entre `Cliente` y `Servicio`, administrando los estados de la reserva y aplicando `try/except/finally` con encadenamiento de excepciones.
- `main.py`: Modulo de integracion que ejecuta 12 operaciones de prueba (transacciones validas e intentos con datos erroneos) para demostrar la estabilidad del sistema.
- `registro_eventos.log`: Archivo generado automaticamente donde se almacenan los eventos del sistema y el registro de errores en tiempo de ejecucion.

## Requisitos y Ejecucion

1. Tener instalado Python 3.8 o superior.
2. Clonar el repositorio y ejecutar el archivo principal:

```bash
python main.py
```
