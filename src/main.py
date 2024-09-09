import csv
import functools
import random
import re
from datetime import datetime


# ------------------- Decoradores -------------------

def registrar_movimiento(funcion):
    """Decorador para registrar movimientos de depósito, retiro y transferencias en un log."""
    @functools.wraps(funcion)
    def wrapper(self, *args, **kwargs):
        try:
            resultado = funcion(self, *args, **kwargs)
            nombre_cliente = self.nombre
            cbu_cliente = self.cbu

            if funcion.__name__ == 'depositar':
                accion = 'Depósito'
                monto = args[0]
            elif funcion.__name__ == 'retirar':
                accion = 'Retiro'
                monto = args[0]
            elif funcion.__name__ == 'transferir':
                accion = 'Transferencia'
                monto = args[0]
            else:
                accion = monto = 'Desconocida'

            # Registro de movimiento en log
            mensaje = (f"{datetime.now():%d/%m/%Y %H:%M} - {nombre_cliente} ({cbu_cliente}) "
                       f"[{accion}] ${monto:.2f}")
            with open('movimientos.log', 'a', encoding='utf-8') as archivo:
                archivo.write(mensaje + '\n')

            return resultado
        except Exception as e:
            print(f"Error al realizar {funcion.__name__}: {e}")
            raise  # Re-lanzamos la excepción para no ocultarla

    return wrapper


# ------------------- Clase Cliente -------------------

class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: int, email: str, saldo: int = 0):
        """Inicialización de un cliente con validaciones."""
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._email = email
        self._saldo = saldo
        self._alias = ""
        random.seed(dni)
        self._cbu = random.randint(10_000, 99_999)

    # Propiedades con validaciones
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not re.match(r"^[A-Za-záéíóúñÀÈÌÒÙÑ\s]+$", valor):
            raise ValueError("El NOMBRE solo puede contener letras y espacios.")
        self._nombre = valor

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str):
        if not re.match(r"^[A-Za-záéíóúñÀÈÌÒÙÑ\s]+$", valor):
            raise ValueError("El Apellido solo puede contener letras y espacios.")
        self._apellido = valor

    @property
    def dni(self) -> int:
        return self._dni

    @dni.setter
    def dni(self, valor: int):
        if not (1 <= valor <= 99_999_999):
            raise ValueError("El DNI debe ser un número entre 1 y 99.999.999.")
        self._dni = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", valor):
            raise ValueError("El formato de email es inválido.")
        self._email = valor

    @property
    def saldo(self) -> int:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: int):
        if valor < 0:
            raise ValueError("El saldo no puede ser negativo.")
        self._saldo = valor

    @property
    def cbu(self) -> int:
        return self._cbu

    @property
    def alias(self) -> str:
        return self._alias

    @alias.setter
    def alias(self, value: str):
        self._alias = value

    # Métodos de operaciones bancarias
    @registrar_movimiento
    def depositar(self, monto: int):
        if monto <= 0:
            raise ValueError("Solo se pueden depositar montos positivos.")
        self.saldo += monto

    @registrar_movimiento
    def retirar(self, monto: int):
        if monto <= 0:
            raise ValueError("El monto para retirar debe ser mayor que 0.")
        if monto > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= monto

    @registrar_movimiento
    def transferir(self, monto: int, destinatario: 'Cliente'):
        if not isinstance(destinatario, Cliente):
            raise ValueError("El destinatario debe ser un Cliente.")
        self.retirar(monto)
        destinatario.depositar(monto)

    def __str__(self) -> str:
        """Representación en formato string del cliente."""
        return (
            f"Cliente: {self.apellido} {self.nombre}\n"
            f"DNI: {self.dni}\n"
            f"Email: {self.email}\n"
            f"Saldo: ${self.saldo:.2f}\n"
            f"CBU: {self.cbu}\n"
            f"Alias: {self.alias}"
        )


# ------------------- Clase Banco -------------------

class Banco:
    def __init__(self):
        """Inicialización de un banco con una lista de clientes."""
        self.clientes: list[Cliente] = []

    def agregar_cliente(self, nombre: str, apellido: str, dni: int, email: str, saldo: int = 0) -> None:
        """Agrega un cliente nuevo al banco."""
        try:
            nuevo_cliente = Cliente(nombre, apellido, dni, email, saldo)
            self.clientes.append(nuevo_cliente)
        except ValueError as e:
            print(f"Error al agregar cliente: {e}")

    def buscar_cliente(self, nombre_o_dni: str | int) -> list[Cliente] | None:
        """Busca clientes por nombre parcial o por DNI."""
        try:
            if isinstance(nombre_o_dni, int):
                return [cliente for cliente in self.clientes if cliente.dni == nombre_o_dni]
            elif isinstance(nombre_o_dni, str):
                return [cliente for cliente in self.clientes if (
                        nombre_o_dni.lower() in cliente.nombre.lower() or nombre_o_dni.lower() in cliente.apellido.lower())]
        except Exception as e:
            print(f"Error al buscar cliente: {e}")
            return []

    def asignar_alias(self, dir_wordlist: str, cliente: Cliente) -> None:
        """Asigna un alias aleatorio a un cliente usando un archivo de lista de palabras."""
        try:
            with open(dir_wordlist, mode="r", encoding="utf-8") as archivo:
                wordlist = [line.strip() for line in archivo]
                cliente.alias = '.'.join(random.sample(wordlist, 3))
        except FileNotFoundError:
            print(f"Archivo de alias '{dir_wordlist}' no encontrado.")
        except Exception as e:
            print(f"Error al asignar alias: {e}")

    def generar_resumen(self, cliente: Cliente) -> str:
        """Genera un resumen de la cuenta del cliente."""
        try:
            return str(cliente)
        except Exception as e:
            print(f"Error al generar resumen: {e}")
            return ""

    def __str__(self) -> str:
        """Genera un resumen de todos los clientes en el banco."""
        try:
            retorno = f"\nCantidad de clientes: {len(self.clientes)}\n"
            for cliente in self.clientes:
                retorno += f"\tNº:{self.clientes.index(cliente)}\n"
                retorno += f"{cliente}\n"
            return retorno
        except Exception as e:
            print(f"Error al generar información del banco: {e}")
            return ""


# ------------------- Función principal -------------------

def main():
    """Función principal que coordina la ejecución del programa."""
    ubicacion_clientes = "clientes.csv"
    ubicacion_palabras_alias = "wordlist.txt"
    banco = Banco()

    # Cargar clientes desde CSV
    cargar_clientes(banco, ubicacion_clientes)

    # Asignar alias a los clientes
    asignar_alias_a_clientes(banco, ubicacion_palabras_alias)

    # Realizar operaciones bancarias
    realizar_operaciones(banco)

    # Mostrar información de clientes y banco
    mostrar_resumenes(banco)


# ------------------- Funciones auxiliares -------------------

def cargar_clientes(banco: Banco, archivo_clientes: str):
    """Carga los clientes desde un archivo CSV."""
    try:
        with open(archivo_clientes, "r", encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                banco.agregar_cliente(row["nombre"], row["apellido"], int(row["dni"]), row["email"])
    except FileNotFoundError:
        print(f"Archivo '{archivo_clientes}' no encontrado.")
    except csv.Error as e:
        print(f"Error al procesar archivo CSV: {e}")
    except Exception as e:
        print(f"Error inesperado al cargar clientes: {e}")


def asignar_alias_a_clientes(banco: Banco, archivo_alias: str):
    """Asigna alias a todos los clientes del banco."""
    try:
        for cliente in banco.clientes:
            banco.asignar_alias(archivo_alias, cliente)
    except Exception as e:
        print(f"Error inesperado al asignar alias: {e}")


def realizar_operaciones(banco: Banco):
    """Realiza algunas operaciones bancarias de prueba."""
    try:
        cliente1 = banco.clientes[0]
        cliente2 = banco.clientes[1]

        cliente1.depositar(1000)
        cliente1.transferir(500, cliente2)
        cliente2.retirar(200)
    except IndexError:
        print("Error: no hay suficientes clientes para realizar las transacciones.")
    except Exception as e:
        print(f"Error en las transacciones: {e}")


def mostrar_resumenes(banco: Banco):
    """Muestra los resúmenes de las cuentas y la información general del banco."""
    try:
        cliente1 = banco.clientes[0]

        resultados = banco.buscar_cliente("ju")
        if resultados:
            print("---- Comienzo de la búsqueda ----")
            for cliente in resultados:
                print(cliente)
            print("---- Fin de la búsqueda ----")
        else:
            print("No se encontraron coincidencias.")

        print(banco.generar_resumen(cliente1))
        print(banco)
    except Exception as e:
        print(f"Error al mostrar resúmenes: {e}")

