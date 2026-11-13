# -*- coding: utf-8 -*-
# Curso: Programacion (213023) - UNAD
# Fase 4 - Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Empresa: Software FJ

# Importamos ABC y abstractmethod para crear las clases abstractas del sistema
from abc import ABC, abstractmethod
# Importamos datetime para registrar la fecha y hora en las entidades y en el archivo de logs
from datetime import datetime


# ==============================================================================
# MODULO 1 - ESTUDIANTE 1: EXCEPCIONES PERSONALIZADAS, LOGS Y CLASE ABSTRACTA BASE
# ==============================================================================

# Clase base para todas las excepciones propias del sistema Software FJ
class SoftwareFJError(Exception):
    # Constructor que recibe el mensaje del error y lo pasa a la clase Exception
    def __init__(self, mensaje):
        super().__init__(mensaje)


# Excepcion para cuando un dato tiene un formato o valor incorrecto (ej. correo sin @)
class DatosInvalidosError(SoftwareFJError):
    pass


# Excepcion para cuando falta un parametro obligatorio (ej. nombre o documento vacio)
class ParametroFaltanteError(SoftwareFJError):
    pass


# Excepcion para cuando se intenta reservar un servicio que ya esta ocupado
class ServicioNoDisponibleError(SoftwareFJError):
    pass


# Excepcion para cuando se intenta hacer una accion no valida segun el estado actual
class OperacionNoPermitidaError(SoftwareFJError):
    pass


# Excepcion para errores en el calculo de tarifas, impuestos, descuentos o duracion
class CalculoInconsistenteError(SoftwareFJError):
    pass


# Clase encargada de escribir todos los eventos y errores en un archivo de texto .log
class GestorLogs:
    # Nombre del archivo donde se guardara el historial de eventos y errores
    ARCHIVO_LOG = "software_fj_eventos.log"

    # Metodo estatico para registrar cualquier mensaje indicando su nivel (INFO, ERROR, etc.)
    @staticmethod
    def registrar(nivel, mensaje):
        # Obtenemos la fecha y hora actual en formato legible
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Armamos la linea de texto que se guardara en el archivo
        linea_log = f"[{fecha_actual}] [{nivel}] {mensaje}\n"
        # Usamos un bloque try/except/finally para asegurar la escritura del archivo
        archivo = None
        try:
            # Abrimos el archivo en modo 'a' (append) para agregar lineas sin borrar las anteriores
            archivo = open(GestorLogs.ARCHIVO_LOG, mode="a", encoding="utf-8")
            # Escribimos la linea en el archivo de logs
            archivo.write(linea_log)
        except OSError as error_archivo:
            # Si ocurre un fallo al abrir o escribir el archivo, lo mostramos por consola
            print(f"[AVISO LOG] No se pudo escribir en el archivo de logs: {error_archivo}")
        finally:
            # En el bloque finally nos aseguramos de cerrar el archivo si fue abierto
            if archivo is not None and not archivo.closed:
                archivo.close()


# Clase abstracta general que representa cualquier entidad del sistema
class EntidadSistema(ABC):
    # Constructor que inicializa los datos basicos de toda entidad
    def __init__(self, id_entidad):
        # Verificamos que el identificador no venga vacio ni con espacios en blanco
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El identificador (ID) de la entidad no puede estar vacio.")
        # Atributo protegido para el identificador unico
        self._id_entidad = str(id_entidad).strip()
        # Atributo protegido con la fecha y hora en que se creo el objeto
        self._fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Propiedad para consultar el id_entidad desde fuera sin modificarlo directamente
    @property
    def id_entidad(self):
        return self._id_entidad

    # Propiedad para consultar la fecha de registro
    @property
    def fecha_registro(self):
        return self._fecha_registro

    # Metodo abstracto que obliga a las clases hijas a validar sus propios datos
    @abstractmethod
    def validar_datos(self):
        pass

    # Metodo abstracto que obliga a las clases hijas a devolver un resumen en texto
    @abstractmethod
    def mostrar_resumen(self):
        pass


# ==============================================================================
# MODULO 2 - ESTUDIANTE 2: CLASE CLIENTE CON ENCAPSULACION Y VALIDACIONES
# ==============================================================================
# Espacio reservado para el Estudiante 2:
# - Crear clase Cliente(EntidadSistema)
# - Definir atributos privados: __documento, __nombre, __correo, __telefono
# - Implementar @property y @setter con validaciones (ParametroFaltanteError y DatosInvalidosError)
# - Implementar validar_datos() y mostrar_resumen()


# ==============================================================================
# MODULO 3 - ESTUDIANTE 3: CLASE ABSTRACTA SERVICIO Y 3 SUBCLASES ESPECIALIZADAS
# ==============================================================================
# Espacio reservado para el Estudiante 3:
# - Crear clase abstracta Servicio(EntidadSistema, ABC)
# - Implementar metodo sobrecargado calcular_costo_total(duracion_horas, impuesto_iva=0.0, descuento_pct=0.0)
# - Crear las 3 clases hijas: ReservaSala, AlquilerEquipo y AsesoriaEspecializada


# ==============================================================================
# MODULO 4 - ESTUDIANTE 4: CLASE RESERVA Y GESTOR CENTRAL EN MEMORIA
# ==============================================================================
# Espacio reservado para el Estudiante 4:
# - Crear clase Reserva(EntidadSistema) con confirmar_reserva(), procesar_reserva() y cancelar_reserva()
# - Crear clase SistemaSoftwareFJ con las listas internas (clientes, servicios, reservas)


# ==============================================================================
# MODULO 5 - ESTUDIANTE 5: SIMULACION SECUENCIAL DE LAS 10 OPERACIONES Y REPORTE
# ==============================================================================
# Espacio reservado para el Estudiante 5:
# - Implementar funcion ejecutar_simulacion() con las 10 operaciones de prueba (validas y fallidas)


if __name__ == "__main__":
    # Prueba inicial de verificacion del Modulo 1
    print("=== Verificacion inicial del Modulo 1 (Excepciones, Logs y EntidadSistema) ===")
    GestorLogs.registrar("INFO", "Prueba inicial del Modulo 1 ejecutada correctamente.")
    print(f"[OK] Archivo de logs '{GestorLogs.ARCHIVO_LOG}' actualizado.")
    print("[OK] Excepciones personalizadas y clase abstracta EntidadSistema listas.")
