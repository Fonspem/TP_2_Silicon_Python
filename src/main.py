import functools
import re
import csv
import random
from datetime import datetime


def registrar_movimiento(funcion):
    @functools.wraps(funcion)
    def wrapper(self, *args, **kwargs):
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
            accion = 'Desconocida'
            monto = 'Desconocido'

        mensaje = (f"{datetime.now():%d/%m/%Y %H:%M} - {nombre_cliente} ({cbu_cliente}) "
                   f"[{accion}] ${monto:.2f}")

        # Escribe el mensaje en el archivo de log
        with open('movimientos.log', 'a', encoding='utf-8') as archivo:
            archivo.write(mensaje + '\n')

        return resultado

    return wrapper

class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: int, email: str, saldo: int = 0):

        self._nombre: str
        self._apellido: str
        self._dni: int
        self._email: str
        self._saldo: int
        self._alias: str = ""
        random.seed(dni)
        self._cbu: int = random.randint(10_000, 99_999)


        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.saldo = saldo

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

    # METODOS-------------------------------------------------------------------

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
        self.clientes:list[Cliente] = []

    def agregar_cliente(self, nombre:str, apellido:str, dni:int, email:str, saldo:int=0)->None:
        nuevo_cliente = Cliente(nombre, apellido, dni, email)
        self.clientes.append(nuevo_cliente)

    def buscar_cliente(self, nombre_o_dni: str | int) -> list[Cliente] | None:
        if isinstance(nombre_o_dni, int):
            return [cliente for cliente in self.clientes if cliente.dni == nombre_o_dni]
        elif isinstance(nombre_o_dni, str):
            return [cliente for cliente in self.clientes if nombre_o_dni.lower() in cliente.nombre.lower() or nombre_o_dni.lower() in cliente.apellido.lower()]

    def asignar_alias(self, dir_wordlist:str, cliente:Cliente)->None:
        with open(dir_wordlist, mode="r", encoding="utf-8") as archivo:
            wordlist =[line.strip() for line in archivo]
            cliente.alias = '.'.join(random.sample(wordlist, 3))

    def generar_resumen(self, cliente:Cliente)->str:
        resumen:str = str(cliente)
        #Probablemente se podria revisar en el log los movimientos para mostrar en el resumen, por eso el formato de la funcion
        return resumen

    def __str__(self)->str:
        retorno:str = f"\nCantidad de clientes: {len(self.clientes)}\n"
        for cliente in self.clientes:
            retorno += f"\tNº:{self.clientes.index(cliente)}\n"
            retorno += f"{str(cliente)}\n"
        return retorno


# Ejemplo de uso
banco = Banco()

# Cargar clientes desde CSV
with open("clientes.csv", "r", encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        try:
            banco.agregar_cliente(row["nombre"], row["apellido"], int(row["dni"]), row["email"])
        except ValueError as e:
            print(e)
# Asignar alias a todos los clientes
for cliente in banco.clientes:
    banco.asignar_alias("wordlist.txt", cliente)

# Realizar algunas operaciones
cliente1 = banco.clientes[0]
cliente2 = banco.clientes[1]

cliente1.depositar(1000)
cliente1.transferir(500, cliente2)
cliente2.retirar(200)

# Buscar cliente por determinado patrón parcial en nombre completo o DNI
# En este caso, buscamos clientes que tengan 'ez' en su nombre completo
resultados = banco.buscar_cliente("ez")
for cliente in resultados:
    print(cliente)

# Generar resumen
print(banco.generar_resumen(cliente1))

# Mostrar información del banco
print(banco)
