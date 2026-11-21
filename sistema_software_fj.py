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
# =====================================================
# Curso: Programacion (213023) - UNAD
# Fase 4 - Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Empresa: Software FJ
# Jazmin Adamary Rativa Moreno 
class Reserva(EntidadSistema):
    """
    Clase que representa una reserva en el sistema Software FJ.
    Integra un Cliente, un Servicio, la duración en horas, el estado y el costo final.
    """

    def __init__(self, id_entidad: str, cliente, servicio, duracion_horas: float):
        super().__init__(id_entidad)

        if cliente is None or not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Debe asociar una instancia válida de Cliente a la reserva.")
        if servicio is None or not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Debe asociar una instancia válida de Servicio a la reserva.")

        try:
            duracion = float(duracion_horas)
        except (TypeError, ValueError) as e:
            raise DatosInvalidosError("La duración en horas debe ser un valor numérico válido.") from e

        if duracion <= 0:
            raise DatosInvalidosError("La duración de la reserva debe ser mayor a cero horas.")

        # Atributos privados según el diagrama UML
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = duracion
        self.__estado = "PENDIENTE"
        self.__costo_final = 0.0

        self.validar_datos()
        GestorLogs.registrar("INFO", f"Reserva '{self._id_entidad}' creada en estado PENDIENTE para el cliente '{self.__cliente.nombre}'.")

    # Propiedades de solo lectura para mantener encapsulación
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion_horas(self):
        return self.__duracion_horas

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_final(self):
        return self.__costo_final

    def validar_datos(self) -> bool:
        """Valida que los datos internos de la reserva sean consistentes."""
        if self.__duracion_horas <= 0:
            raise DatosInvalidosError("La duración en horas debe ser mayor a cero.")
        if self.__estado not in ["PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA"]:
            raise DatosInvalidosError(f"Estado de reserva inválido: {self.__estado}")
        return True

    def confirmar_reserva(self):
        """
        Confirma una reserva pendiente verificando que el servicio esté disponible.
        """
        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva '{self._id_entidad}' porque su estado actual es '{self.__estado}'."
            )

        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__servicio.nombre_servicio}' (ID: {self.__servicio.id_entidad}) no está disponible."
            )

        self.__estado = "CONFIRMADA"
        self.__servicio.disponible = False
        GestorLogs.registrar("INFO", f"Reserva '{self._id_entidad}' CONFIRMADA. Servicio '{self.__servicio.id_entidad}' bloqueado.")

    def procesar_reserva(self, iva: float = 0.19, descuento: float = 0.0) -> float:
        """
        Procesa una reserva confirmada calculando su costo final con IVA y descuento opcionales.
        Implementa encadenamiento de excepciones y bloque try/except/else.
        """
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas en estado 'CONFIRMADA'. Estado actual: '{self.__estado}'."
            )

        try:
            costo_calculado = self.__servicio.calcular_costo_total(
                duracion_horas=self.__duracion_horas,
                impuesto_iva=iva,
                descuento_pct=descuento
            )
        except SoftwareFJError as e:
            GestorLogs.registrar("ERROR", f"Fallo al procesar reserva '{self._id_entidad}': {e}")
            raise CalculoInconsistenteError(
                f"No fue posible calcular el costo final de la reserva '{self._id_entidad}'."
            ) from e
        else:
            self.__costo_final = costo_calculado
            self.__estado = "PROCESADA"
            self.__servicio.disponible = True  # Libera el servicio tras finalizar el proceso
            GestorLogs.registrar(
                "INFO",
                f"Reserva '{self._id_entidad}' PROCESADA exitosamente. Costo final: ${self.__costo_final:.2f}"
            )
            return self.__costo_final

    def cancelar_reserva(self, motivo: str):
        """
        Cancela una reserva si aún no ha sido procesada ni cancelada previamente.
        """
        if not motivo or not str(motivo).strip():
            raise ParametroFaltanteError("Debe indicar un motivo válido para cancelar la reserva.")

        if self.__estado in ["PROCESADA", "CANCELADA"]:
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva '{self._id_entidad}' porque ya está '{self.__estado}'."
            )

        estado_anterior = self.__estado
        self.__estado = "CANCELADA"

        # Si estaba confirmada, devolvemos la disponibilidad al servicio
        if estado_anterior == "CONFIRMADA":
            self.__servicio.disponible = True

        GestorLogs.registrar(
            "INFO",
            f"Reserva '{self._id_entidad}' CANCELADA. Motivo: {str(motivo).strip()}"
        )

    def mostrar_resumen(self) -> str:
        """Devuelve un resumen detallado del estado actual de la reserva."""
        return (
            f"[Reserva ID: {self._id_entidad}] Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre_servicio} ({self.__servicio.id_entidad}) | "
            f"Duración: {self.__duracion_horas}h | Estado: {self.__estado} | "
            f"Costo Final: ${self.__costo_final:.2f}"
        )


class SistemaSoftwareFJ:
    """
    Gestor central en memoria que administra las listas internas de clientes,
    servicios y reservas sin utilizar bases de datos.
    """

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        GestorLogs.registrar("INFO", "SistemaSoftwareFJ inicializado en memoria correctamente.")

    # Propiedades para consultar copias seguras de las listas internas
    @property
    def clientes(self):
        return list(self.__clientes)

    @property
    def servicios(self):
        return list(self.__servicios)

    @property
    def reservas(self):
        return list(self.__reservas)

    # --- Gestión de Clientes ---
    def registrar_cliente(self, cliente) -> bool:
        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError("El objeto proporcionado no corresponde a un Cliente válido.")
            if any(c.id_entidad == cliente.id_entidad or c.documento == cliente.documento for c in self.__clientes):
                raise OperacionNoPermitidaError(
                    f"Ya existe un cliente registrado con ID '{cliente.id_entidad}' o documento '{cliente.documento}'."
                )
            cliente.validar_datos()
        except SoftwareFJError as e:
            GestorLogs.registrar("ERROR", f"Error al registrar cliente: {e}")
            raise
        else:
            self.__clientes.append(cliente)
            GestorLogs.registrar("INFO", f"Cliente '{cliente.nombre}' (ID: {cliente.id_entidad}) registrado en el sistema.")
            return True

    def buscar_cliente(self, id_cliente: str):
        for cliente in self.__clientes:
            if cliente.id_entidad == str(id_cliente).strip():
                return cliente
        raise ParametroFaltanteError(f"No se encontró ningún cliente con ID '{id_cliente}'.")

    # --- Gestión de Servicios ---
    def registrar_servicio(self, servicio) -> bool:
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto proporcionado no corresponde a un Servicio válido.")
            if any(s.id_entidad == servicio.id_entidad for s in self.__servicios):
                raise OperacionNoPermitidaError(
                    f"Ya existe un servicio registrado con ID '{servicio.id_entidad}'."
                )
            servicio.validar_datos()
        except SoftwareFJError as e:
            GestorLogs.registrar("ERROR", f"Error al registrar servicio: {e}")
            raise
        else:
            self.__servicios.append(servicio)
            GestorLogs.registrar("INFO", f"Servicio '{servicio.nombre_servicio}' (ID: {servicio.id_entidad}) registrado en el sistema.")
            return True

    def buscar_servicio(self, id_servicio: str):
        for servicio in self.__servicios:
            if servicio.id_entidad == str(id_servicio).strip():
                return servicio
        raise ParametroFaltanteError(f"No se encontró ningún servicio con ID '{id_servicio}'.")

    # --- Gestión de Reservas ---
    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, duracion_horas: float) -> Reserva:
        try:
            if any(r.id_entidad == str(id_reserva).strip() for r in self.__reservas):
                raise OperacionNoPermitidaError(f"Ya existe una reserva con ID '{id_reserva}'.")

            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)

            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre_servicio}' (ID: {servicio.id_entidad}) no está disponible para reservar."
                )

            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)
        except SoftwareFJError as e:



# ==============================================================================
# MODULO 5 - ESTUDIANTE 5: SIMULACION SECUENCIAL DE LAS 10 OPERACIONES Y REPORTE
# ==============================================================================
#def ejecutar_simulacion():
    """
    Ejecuta de forma secuencial las 10 operaciones de prueba (casos válidos
    y errores controlados) para verificar la estabilidad del sistema Software FJ.
    """
    print("\n" + "=" * 75)
    print("INICIO DE SIMULACIÓN - SISTEMA INTEGRAL SOFTWARE FJ (10 OPERACIONES)")
    print("=" * 75)

    sistema = SistemaSoftwareFJ()
    cliente_ana = None
    cliente_carlos = None
    sala_juntas = None
    alquiler_portatiles = None
    asesoria_dev = None
    reserva_sala_ana = None
    reserva_portatiles_carlos = None
    reserva_asesoria_error = None

    # 1. Registro válido de clientes: Ana Gómez y Carlos Pérez
    print("\n--- Operación 1: Registro válido de clientes (Ana Gómez y Carlos Pérez) ---")
    try:
        cliente_ana = Cliente("CLI-001", "1010203040", "Ana Gómez", "ana.gomez@softwarefj.com", "3001112233")
        cliente_carlos = Cliente("CLI-002", "1020304050", "Carlos Pérez", "carlos.perez@softwarefj.com", "3004445566")
        sistema.registrar_cliente(cliente_ana)
        sistema.registrar_cliente(cliente_carlos)
        print("[OK] Clientes Ana Gómez y Carlos Pérez registrados correctamente.")
    except SoftwareFJError as e:
        print(f"[ERROR INESPERADO] {e}")

    # 2. Error controlado en cliente (correo sin '@') -> DatosInvalidosError
    print("\n--- Operación 2: Error controlado en cliente (correo sin '@') ---")
    try:
        cliente_mal_correo = Cliente("CLI-003", "1030405060", "Luis Torres", "correo_invalido.com", "3007778899")
        sistema.registrar_cliente(cliente_mal_correo)
    except DatosInvalidosError as e:
        GestorLogs.registrar("ERROR", f"Op. 2 controlada (DatosInvalidosError): {e}")
        print(f"[OK - CAPTURADO DatosInvalidosError] {e}")
    except SoftwareFJError as e:
        print(f"[ERROR] Excepción distinta a la esperada: {e}")

    # 3. Error controlado en cliente (documento en blanco) -> ParametroFaltanteError
    print("\n--- Operación 3: Error controlado en cliente (documento en blanco) ---")
    try:
        cliente_sin_doc = Cliente("CLI-004", "   ", "Sofía Ruiz", "sofia.ruiz@softwarefj.com", "3009990011")
        sistema.registrar_cliente(cliente_sin_doc)
    except ParametroFaltanteError as e:
        GestorLogs.registrar("ERROR", f"Op. 3 controlada (ParametroFaltanteError): {e}")
        print(f"[OK - CAPTURADO ParametroFaltanteError] {e}")
    except SoftwareFJError as e:
        print(f"[ERROR] Excepción distinta a la esperada: {e}")

    # 4. Creación válida de servicios: sala de juntas, alquiler de portátiles y asesoría de desarrollo
    print("\n--- Operación 4: Creación válida de servicios ---")
    try:
        sala_juntas = ReservaSala("SRV-SALA-1", tarifa_base_hora=80.0, capacidad_personas=12, incluye_multimedia=True)
        alquiler_portatiles = AlquilerEquipo("SRV-EQ-1", tarifa_base_hora=25.0, tipo_equipo="Portátiles", cantidad_unidades=4, incluye_seguro=True)
        asesoria_dev = AsesoriaEspecializada("SRV-ASE-1", tarifa_base_hora=100.0, area_tematica="Desarrollo", nivel_experto="SENIOR")
        sistema.registrar_servicio(sala_juntas)
        sistema.registrar_servicio(alquiler_portatiles)
        sistema.registrar_servicio(asesoria_dev)
        print("[OK] Servicios (Sala de juntas, Alquiler de portátiles y Asesoría de desarrollo) registrados.")
    except SoftwareFJError as e:
        print(f"[ERROR INESPERADO] {e}")

    # 5. Error controlado en servicio: sala con capacidad de -10 personas
    print("\n--- Operación 5: Error controlado en servicio (capacidad -10 personas) ---")
    try:
        sala_invalida = ReservaSala("SRV-SALA-ERR", tarifa_base_hora=80.0, capacidad_personas=-10, incluye_multimedia=False)
        sistema.registrar_servicio(sala_invalida)
    except DatosInvalidosError as e:
        GestorLogs.registrar("ERROR", f"Op. 5 controlada (DatosInvalidosError): {e}")
        print(f"[OK - CAPTURADO DatosInvalidosError] {e}")
    except SoftwareFJError as e:
        print(f"[ERROR] Excepción distinta a la esperada: {e}")

    # 6. Reserva exitosa (costo básico): sala de juntas para Ana Gómez por 3 horas sin impuestos ni descuentos
    print("\n--- Operación 6: Reserva exitosa (costo básico - Ana Gómez, 3h) ---")
    try:
        reserva_sala_ana = sistema.crear_reserva("RES-001", "CLI-001", "SRV-SALA-1", 3.0)
        reserva_sala_ana.confirmar_reserva()
        costo_basico = reserva_sala_ana.procesar_reserva(iva=0.0, descuento=0.0)
        print(f"[OK] Reserva confirmada y procesada. Costo total (sin IVA ni descuento): ${costo_basico:.2f}")
    except SoftwareFJError as e:
        print(f"[ERROR INESPERADO] {e}")

    # 7. Error por servicio ocupado: intentar reservar la misma sala de juntas para Carlos Pérez
    print("\n--- Operación 7: Error por servicio ocupado (Carlos Pérez -> misma sala) ---")
    try:
        # Bloqueamos temporalmente la disponibilidad para simular que sigue ocupada tras la Op. 6
        sala_juntas.disponible = False
        reserva_duplicada = sistema.crear_reserva("RES-002", "CLI-002", "SRV-SALA-1", 2.0)
        reserva_duplicada.confirmar_reserva()
    except ServicioNoDisponibleError as e:
        GestorLogs.registrar("ERROR", f"Op. 7 controlada (ServicioNoDisponibleError): {e}")
        print(f"[OK - CAPTURADO ServicioNoDisponibleError] {e}")
    except SoftwareFJError as e:
        print(f"[ERROR] Excepción distinta a la esperada: {e}")

    # 8. Reserva exitosa con sobrecarga (IVA 19% y descuento 10%): portátiles para Carlos Pérez
    print("\n--- Operación 8: Reserva exitosa con sobrecarga (IVA 19%, Desc. 10% - Carlos Pérez) ---")
    try:
        reserva_portatiles_carlos = sistema.crear_reserva("RES-003", "CLI-002", "SRV-EQ-1", 4.0)
        reserva_portatiles_carlos.confirmar_reserva()
        costo_con_sobrecarga = reserva_portatiles_carlos.procesar_reserva(iva=0.19, descuento=0.10)
        print(f"[OK] Reserva de portátiles procesada con IVA 19% y descuento 10%. Total: ${costo_con_sobrecarga:.2f}")
    except SoftwareFJError as e:
        print(f"[ERROR INESPERADO] {e}")

    # 9. Error en cálculo de costos (encadenamiento): asesoría con descuento inválido (150% -> 1.50)
    print("\n--- Operación 9: Error en cálculo de costos (descuento 150% / 1.50) ---")
    try:
        reserva_asesoria_error = sistema.crear_reserva("RES-004", "CLI-001", "SRV-ASE-1", 2.0)
        reserva_asesoria_error.confirmar_reserva()
        reserva_asesoria_error.procesar_reserva(iva=0.19, descuento=1.50)
    except CalculoInconsistenteError as e:
        causa = e.__cause__
        GestorLogs.registrar("ERROR", f"Op. 9 controlada (CalculoInconsistenteError): {e} | Causa: {causa}")
        print(f"[OK - CAPTURADO CalculoInconsistenteError] {e}")
        if causa is not None:
            print(f"    Causa encadenada (__cause__): {type(causa).__name__}: {causa}")
    except SoftwareFJError as e:
        print(f"[ERROR] Excepción distinta a la esperada: {e}")

    # 10. Cancelación y validación de estado: cancelar reserva activa y luego intentar cancelarla de nuevo
    print("\n--- Operación 10: Cancelación y validación de estado (doble cancelación) ---")
    reserva_cancelable = None
    try:
        reserva_cancelable = sistema.crear_reserva("RES-005", "CLI-002", "SRV-ASE-1", 1.5)
        reserva_cancelable.confirmar_reserva()
        reserva_cancelable.cancelar_reserva("Cambio de agenda del cliente")
        print("[OK] Primera cancelación realizada con éxito.")
    except SoftwareFJError as e:
        print(f"[ERROR INESPERADO] {e}")

    try:
        if reserva_cancelable is not None:
            reserva_cancelable.cancelar_reserva("Intento de segunda cancelación")
    except OperacionNoPermitidaError as e:
        GestorLogs.registrar("ERROR", f"Op. 10 controlada (OperacionNoPermitidaError): {e}")
        print(f"[OK - CAPTURADO OperacionNoPermitidaError] {e}")
    except SoftwareFJError as e:
        print(f"[ERROR] Excepción distinta a la esperada: {e}")

    # Resumen final en consola
    print("\n" + "=" * 75)
    print("RESUMEN FINAL DEL SISTEMA EN MEMORIA")
    print("=" * 75)
    print(f"Total clientes registrados: {len(sistema.clientes)}")
    for c in sistema.clientes:
        print(f"  - ID: {c.id_entidad} | Nombre: {c.nombre} | Correo: {c.correo}")

    print(f"\nTotal servicios registrados: {len(sistema.servicios)}")
    for s in sistema.servicios:
        print(f"  - {s.mostrar_resumen()} | Disponible: {s.disponible}")

    print(f"\nTotal reservas creadas: {len(sistema.reservas)}")
    for r in sistema.reservas:
        print(f"  - {r.mostrar_resumen()}")

    print(f"\nHistorial de eventos y errores guardado en: '{GestorLogs.ARCHIVO_LOG}'")
    print("=" * 75)


if __name__ == "__main__":
    ejecutar_simulacion()


if __name__ == "__main__":
    # Prueba inicial de verificacion del Modulo 1
    print("=== Verificacion inicial del Modulo 1 (Excepciones, Logs y EntidadSistema) ===")
    GestorLogs.registrar("INFO", "Prueba inicial del Modulo 1 ejecutada correctamente.")
    print(f"[OK] Archivo de logs '{GestorLogs.ARCHIVO_LOG}' actualizado.")
    print("[OK] Excepciones personalizadas y clase abstracta EntidadSistema listas.")
