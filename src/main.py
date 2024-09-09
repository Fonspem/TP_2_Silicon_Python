import csv
import functools
import random
import re
from datetime import datetime

def registrar_movimiento(funcion):
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
            print(f"Error al realizar log: {e}")
    return wrapper


class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: int, email: str, saldo: int = 0):
        self._nombre:str
        self._apellido:str
        self._dni:int
        self._email:str
        self._saldo:int
        self._alias:str

        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.saldo = saldo
        self.alias = ""
        random.seed(dni)
        self._cbu = random.randint(10_000, 99_999)

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
        return (
            f"Cliente: {self.apellido} {self.nombre}\n"
            f"DNI: {self.dni}\n"
            f"Email: {self.email}\n"
            f"Saldo: ${self.saldo:.2f}\n"
            f"CBU: {self.cbu}\n"
            f"Alias: {self.alias}"
        )

class Banco:
    def __init__(self):
        self.clientes: list[Cliente] = []

    def agregar_cliente(self, nombre: str, apellido: str, dni: int, email: str, saldo: int = 0) -> None:
        try:
            nuevo_cliente = Cliente(nombre, apellido, dni, email, saldo)
            self.clientes.append(nuevo_cliente)
        except ValueError as e:
            print(f"Error al agregar cliente: {e}")

    def buscar_cliente(self, nombre_o_dni: str | int) -> list[Cliente] | None:
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
        try:
            with open(dir_wordlist, mode="r", encoding="utf-8") as archivo:
                wordlist = [line.strip() for line in archivo]
                cliente.alias = '.'.join(random.sample(wordlist, 3))
        except FileNotFoundError:
            print(f"Archivo de alias '{dir_wordlist}' no encontrado.")
        except Exception as e:
            print(f"Error al asignar alias: {e}")

    def generar_resumen(self, cliente: Cliente) -> str:
        try:
            return str(cliente)
        except Exception as e:
            print(f"Error al generar resumen: {e}")
            return ""

    def __str__(self) -> str:
        try:
            retorno = f"\nCantidad de clientes: {len(self.clientes)}\n"
            for cliente in self.clientes:
                retorno += f"\tNº:{self.clientes.index(cliente)}\n"
                retorno += f"{cliente}\n"
            return retorno
        except Exception as e:
            print(f"Error al generar información del banco: {e}")
            return ""

def main():
    
    ubicacion_clientes = "clientes.csv"
    ubicacion_palabras_alias = "wordlist.txt"
    banco = Banco()

    #Cargamos los clientes
    try:
        with open(ubicacion_clientes, "r", encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                banco.agregar_cliente(row["nombre"], row["apellido"], int(row["dni"]), row["email"])
    except FileNotFoundError:
        print(f"Archivo '{ubicacion_clientes}' no encontrado.")
    except Exception as e:
        print(f"Error al cargar clientes: {e}")

    try:
        for cliente in banco.clientes:
            banco.asignar_alias(ubicacion_palabras_alias, cliente)
    except Exception as e:
        print(f"Error al asignar alias: {e}")

    try:
        cliente1 = banco.clientes[0]
        cliente2 = banco.clientes[1]

        cliente1.depositar(1000)
        cliente1.transferir(500, cliente2)
        cliente2.retirar(200)
    except IndexError:
        #si no se encuentra el archivo de clientes o son muy pocos
        print("Error: no hay suficientes clientes para realizar las transacciones.")
    except Exception as e:
        print(f"Error en las transacciones: {e}")

    try:
        cliente1 = banco.clientes[0]

        resultados = banco.buscar_cliente("ez")
        if resultados:
            print("---- Comienzo de la búsqueda ----")
            for cliente in resultados:
                print(cliente)
            print("---- Fin de la búsqueda ----")
        else:
            print("No se encontraron coincidencias.")

        input("Enter para continuar")

        print("/nResumen de la cuenta:")
        print(banco.generar_resumen(cliente1))

        input("Enter para continuar")

        print("/nPrint del banco:")
        print(banco)
    except Exception as e:
        print(f"Error al mostrar resúmenes: {e}")


if __name__ == "__main__":
    main()