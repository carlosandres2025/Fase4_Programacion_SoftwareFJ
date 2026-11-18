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
class Cliente(EntidadSistema):
    
    """
    Clase que representa a un cliente dentro del sistema Software FJ.
    Hereda de la clase abstracta EntidadSistema y aplica encapsulación estricta
    mediante atributos privados (__), propiedades (@property/@setter) y
    manejo de excepciones personalizadas.
    """

    def __init__(
        self,
        id_cliente: str,
        documento: str,
        nombre: str,
        correo: str,
        telefono: str,
    ):
        """
        Constructor de la clase Cliente.
        Inicializa los atributos heredados y los atributos propios del cliente
        pasando cada dato por su respectivo setter para garantizar la validación.
        """
        # Invoca el constructor de la clase padre (EntidadSistema) para asignar el ID y la fecha de registro
        super().__init__(id_cliente)

        # Asigna el documento invocando al método setter @documento.setter (ejecuta validación)
        self.documento = documento

        # Asigna el nombre invocando al método setter @nombre.setter (ejecuta validación)
        self.nombre = nombre

        # Asigna el correo invocando al método setter @correo.setter (ejecuta validación)
        self.correo = correo

        # Asigna el teléfono invocando al método setter @telefono.setter (ejecuta validación)
        self.telefono = telefono

        # Ejecuta una validación integral final para asegurar que toda la entidad sea consistente
        self.validar_datos()

    # --------------------------------------------------------------------------
    # PROPIEDADES Y SETTERS (Encapsulación y Validación de Datos)
    # --------------------------------------------------------------------------

    @property
    def documento(self) -> str:
        """Método getter que permite leer de forma segura el atributo privado __documento."""
        # Retorna el valor almacenado en el atributo privado __documento
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        """Método setter que valida y modifica el atributo privado __documento."""
        # Verifica si el valor es nulo (None) o si al quitarle espacios queda una cadena vacía
        if not valor or not str(valor).strip():
            # Lanza la excepción personalizada ParametroFaltanteError si el dato está vacío
            raise ParametroFaltanteError(
                "El documento del cliente es obligatorio."
            )

        # Convierte el valor a cadena de texto y elimina espacios en blanco al inicio y al final
        valor_limpio = str(valor).strip()

        # Verifica si todos los caracteres de la cadena son dígitos numéricos (0-9)
        if not valor_limpio.isdigit():
            # Lanza DatosInvalidosError si el documento contiene letras, símbolos o espacios internos
            raise DatosInvalidosError(
                f"El documento '{valor_limpio}' debe contener solo caracteres numéricos."
            )

        # Si supera todas las validaciones, guarda el dato limpio en el atributo privado __documento
        self.__documento = valor_limpio

    @property
    def nombre(self) -> str:
        """Método getter que permite leer de forma segura el atributo privado __nombre."""
        # Retorna el valor almacenado en el atributo privado __nombre
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Método setter que valida y modifica el atributo privado __nombre."""
        # Comprueba que el nombre recibido no sea nulo ni una cadena compuesta solo por espacios
        if not valor or not str(valor).strip():
            # Lanza ParametroFaltanteError indicando que el campo nombre es requerido
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")

        # Limpia los espacios sobrantes en los extremos del nombre recibido
        valor_limpio = str(valor).strip()

        # Comprueba que el nombre tenga una longitud mínima razonable (al menos 3 caracteres)
        if len(valor_limpio) < 3:
            # Lanza DatosInvalidosError si el nombre es demasiado corto
            raise DatosInvalidosError(
                "El nombre del cliente debe tener al menos 3 caracteres."
            )

        # Almacena el nombre validado en el atributo privado __nombre
        self.__nombre = valor_limpio

    @property
    def correo(self) -> str:
        """Método getter que permite leer de forma segura el atributo privado __correo."""
        # Retorna el valor almacenado en el atributo privado __correo
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Método setter que valida y modifica el atributo privado __correo."""
        # Verifica que el correo no sea None y que no esté vacío tras eliminar espacios
        if not valor or not str(valor).strip():
            # Lanza ParametroFaltanteError si no se proporcionó un correo electrónico
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")

        # Elimina espacios en blanco innecesarios al inicio y final del correo
        valor_limpio = str(valor).strip()

        # Valida que exista el símbolo '@' y que después del '@' exista al menos un punto '.' para el dominio
        if "@" not in valor_limpio or "." not in valor_limpio.split("@")[-1]:
            # Lanza DatosInvalidosError si el correo no cumple con la estructura básica usuario@dominio.ext
            raise DatosInvalidosError(
                f"El correo '{valor_limpio}' no tiene un formato válido (debe incluir '@' y dominio)."
            )

        # Guarda el correo electrónico validado en el atributo privado __correo
        self.__correo = valor_limpio

    @property
    def telefono(self) -> str:
        """Método getter que permite leer de forma segura el atributo privado __telefono."""
        # Retorna el valor almacenado en el atributo privado __telefono
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Método setter que valida y modifica el atributo privado __telefono."""
        # Comprueba que el teléfono no sea nulo ni esté compuesto únicamente de espacios
        if not valor or not str(valor).strip():
            # Lanza ParametroFaltanteError si el teléfono viene vacío
            raise ParametroFaltanteError(
                "El teléfono del cliente es obligatorio."
            )

        # Convierte a texto y limpia espacios en los extremos
        valor_limpio = str(valor).strip()

        # Valida que el número telefónico contenga exclusivamente dígitos numéricos
        if not valor_limpio.isdigit():
            # Lanza DatosInvalidosError si contiene letras, guiones o caracteres especiales
            raise DatosInvalidosError(
                f"El teléfono '{valor_limpio}' debe contener solo caracteres numéricos."
            )

        # Asigna el teléfono validado al atributo privado __telefono
        self.__telefono = valor_limpio

    # --------------------------------------------------------------------------
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS (Polimorfismo desde EntidadSistema)
    # --------------------------------------------------------------------------

    def validar_datos(self) -> bool:
        """
        Implementación obligatoria del método abstracto validar_datos() de EntidadSistema.
        Verifica de manera integral que todos los atributos del cliente existan y sean válidos.
        """
        # Inicia bloque try para capturar y gestionar cualquier falla durante la verificación
        try:
            # Verifica que el atributo protegido _id_entidad (heredado) no esté vacío
            if not self._id_entidad or not str(self._id_entidad).strip():
                # Lanza ParametroFaltanteError si falta el identificador único del cliente
                raise ParametroFaltanteError(
                    "El ID del cliente no puede estar vacío."
                )

            # Comprueba que los cuatro atributos privados tengan valores asignados y no vacíos
            if not (
                self.__documento
                and self.__nombre
                and self.__correo
                and self.__telefono
            ):
                # Lanza ParametroFaltanteError si alguno de los atributos privados está incompleto
                raise ParametroFaltanteError(
                    "Faltan datos obligatorios en el perfil del cliente."
                )

            # Si todas las comprobaciones son exitosas, retorna True indicando validez
            return True

        # Captura cualquier excepción ocurrida dentro del bloque try
        except Exception as error_origen:
            # Si la excepción ya es una de las excepciones personalizadas esperadas, la relanza tal cual
            if isinstance(
                error_origen, (ParametroFaltanteError, DatosInvalidosError)
            ):
                raise
            # Si ocurre un error no previsto (ej. AttributeError), aplica encadenamiento de excepciones
            raise DatosInvalidosError(
                "Error inesperado al validar los datos del cliente."
            ) from error_origen

    def mostrar_resumen(self) -> str:
        """
        Implementación obligatoria del método abstracto mostrar_resumen() de EntidadSistema.
        Construye y retorna una cadena de texto legible con los datos principales del cliente.
        """
        # Formatea y retorna los atributos heredados (_id_entidad, _fecha_registro) y los privados (__nombre, etc.)
        return (
            f"[Cliente ID: {self._id_entidad} | Registro: {self._fecha_registro}] "




# ==============================================================================
# MODULO 3 - ESTUDIANTE 3: CLASE ABSTRACTA SERVICIO Y 3 SUBCLASES ESPECIALIZADAS
# ==============================================================================

class Servicio(EntidadSistema, ABC):
    """
    Clase abstracta que hereda de EntidadSistema y sirve como base 
    para todos los servicios ofrecidos por Software FJ.
    """
    def __init__(self, id_entidad: str, nombre_servicio: str, tarifa_base_hora: float):
        super().__init__(id_entidad)
        if not nombre_servicio or not str(nombre_servicio).strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        if tarifa_base_hora <= 0:
            raise DatosInvalidosError("La tarifa base por hora debe ser mayor a cero.")
            
        self._nombre_servicio = str(nombre_servicio).strip()
        self._tarifa_base_hora = float(tarifa_base_hora)
        self._disponible = True  # Por defecto el servicio está disponible

    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @property
    def tarifa_base_hora(self):
        return self._tarifa_base_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: float) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    def calcular_costo_total(self, duracion_horas: float, impuesto_iva: float = 0.0, descuento_pct: float = 0.0) -> float:
        """
        Método sobrecargado para calcular el costo total aplicando IVA y descuentos opcionales.
        Incluye manejo de validaciones y encadenamiento de excepciones si los valores son inconsistentes.
        """
        try:
            if duracion_horas <= 0:
                raise ValueError("La duración en horas debe ser mayor a cero.")
            if not (0.0 <= impuesto_iva <= 1.0) or not (0.0 <= descuento_pct <= 1.0):
                raise ValueError("Los porcentajes de IVA o descuento deben estar entre 0.0 y 1.0.")
            
            costo_base = self.calcular_costo_base(duracion_horas)
            subtotal = costo_base * (1.0 - descuento_pct)
            total = subtotal * (1.0 + impuesto_iva)
            return round(total, 2)
        except ValueError as e:
            GestorLogs.registrar("ERROR", f"Error en cálculo de costos para {self._nombre_servicio}: {e}")
            raise CalculoInconsistenteError(f"Error al calcular el costo total para el servicio '{self._nombre_servicio}'") from e


class ReservaSala(Servicio):
    """Clase derivada para la reserva de salas de juntas o reuniones."""
    def __init__(self, id_entidad: str, tarifa_base_hora: float, capacidad_personas: int, incluye_multimedia: bool):
        super().__init__(id_entidad, "Reserva de Sala", tarifa_base_hora)
        self._capacidad_personas = int(capacidad_personas)
        self._incluye_multimedia = bool(incluye_multimedia)
        self.validar_datos()

    def validar_datos(self) -> bool:
        if self._capacidad_personas <= 0:
            raise DatosInvalidosError("La capacidad de personas en la sala debe ser mayor a cero.")
        return True

    def mostrar_resumen(self) -> str:
        multimedia_str = "Sí" if self._incluye_multimedia else "No"
        return f"[Sala ID: {self._id_entidad}] {self._nombre_servicio} - Capacidad: {self._capacidad_personas} pers. - Multimedia: {multimedia_str} - Tarifa/h: ${self._tarifa_base_hora}"

    def calcular_costo_base(self, duracion_horas: float) -> float:
        self.validar_datos()
        costo = self._tarifa_base_hora * duracion_horas
        if self._incluye_multimedia:
            costo += 15.0 * duracion_horas  # Recargo fijo por hora si incluye multimedia
        return costo


class AlquilerEquipo(Servicio):
    """Clase derivada para el alquiler de equipos tecnológicos."""
    def __init__(self, id_entidad: str, tarifa_base_hora: float, tipo_equipo: str, cantidad_unidades: int, incluye_seguro: bool):
        super().__init__(id_entidad, "Alquiler de Equipo", tarifa_base_hora)
        self._tipo_equipo = str(tipo_equipo)
        self._cantidad_unidades = int(cantidad_unidades)
        self._incluye_seguro = bool(incluye_seguro)
        self.validar_datos()

    def validar_datos(self) -> bool:
        if not self._tipo_equipo.strip():
            raise ParametroFaltanteError("El tipo de equipo no puede estar vacío.")
        if self._cantidad_unidades <= 0:
            raise DatosInvalidosError("La cantidad de unidades a alquilar debe ser mayor a cero.")
        return True

    def mostrar_resumen(self) -> str:
        seguro_str = "Sí" if self._incluye_seguro else "No"
        return f"[Equipo ID: {self._id_entidad}] {self._nombre_servicio}: {self._tipo_equipo} (x{self._cantidad_unidades}) - Seguro: {seguro_str} - Tarifa/h: ${self._tarifa_base_hora}"

    def calcular_costo_base(self, duracion_horas: float) -> float:
        self.validar_datos()
        costo_unitario = self._tarifa_base_hora * duracion_horas
        costo_total = costo_unitario * self._cantidad_unidades
        if self._incluye_seguro:
            costo_total *= 1.08  # Incremento del 8% si incluye seguro contra daños
        return costo_total


class AsesoriaEspecializada(Servicio):
    """Clase derivada para asesorías técnicas especializadas (Junior / Senior)."""
    def __init__(self, id_entidad: str, tarifa_base_hora: float, area_tematica: str, nivel_experto: str):
        super().__init__(id_entidad, "Asesoría Especializada", tarifa_base_hora)
        self._area_tematica = str(area_tematica)
        self._nivel_experto = str(nivel_experto).upper()
        self.validar_datos()

    def validar_datos(self) -> bool:
        if not self._area_tematica.strip():
            raise ParametroFaltanteError("El área temática de la asesoría no puede estar vacía.")
        if self._nivel_experto not in ["JUNIOR", "SENIOR"]:
            raise DatosInvalidosError("El nivel experto debe ser estrictamente 'JUNIOR' o 'SENIOR'.")
        return True

    def mostrar_resumen(self) -> str:
        return f"[Asesoría ID: {self._id_entidad}] {self._nombre_servicio} en {self._area_tematica} - Nivel: {self._nivel_experto} - Tarifa base/h: ${self._tarifa_base_hora}"

    def calcular_costo_base(self, duracion_horas: float) -> float:
        self.validar_datos()
        tarifa_efectiva = self._tarifa_base_hora
        if self._nivel_experto == "SENIOR":
            tarifa_efectiva *= 1.5  # Factor multiplicador de 1.5x para consultores Senior
        return tarifa_efectiva * duracion_horas


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
