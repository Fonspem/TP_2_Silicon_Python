
import csv
import random
import re
from datetime import datetime
import functools

# Rutas a los archivos
clientes_csv = "clientes.csv"
wordlist_txt = "wordlist.txt"


# 2.1 Clase Cliente
class Cliente:
    def __init__(self, nombre, apellido, dni, email):
        self._nombre = ""
        self.nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._email = email
        self._saldo = 0
        self._cbu = self.generar_cbu()
        self._alias = None

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if re.match(r'^[a-zA-Z\s]+$', valor):
            self._nombre = valor
        else:
            raise ValueError("El nombre solo puede contener letras y espacios.")

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        if re.match(r'^[a-zA-Z\s]+$', valor):
            self._apellido = valor
        else:
            raise ValueError("El apellido solo puede contener letras y espacios.")

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, valor):
        if 1 <= valor <= 99999999:
            self._dni = valor
        else:
            raise ValueError("El DNI debe ser un número entre 1 y 99.999.999")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$', valor):
            self._email = valor
        else:
            raise ValueError("El email no es válido.")

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self._saldo = valor
        else:
            raise ValueError("El saldo no puede ser negativo.")

    def generar_cbu(self):
        return str(random.randint(10000, 99999))

    @property
    def cbu(self):
        return self._cbu

    @property
    def alias(self):
        return self._alias

    def asignar_alias(self, wordlist):
        palabras = random.sample(wordlist, 3)
        self._alias = '.'.join(palabras)

    @registrar_movimiento
    def depositar(self, monto):
        if monto > 0:
            self._saldo += monto
            print(f"Se han depositado ${monto}. Saldo actual: ${self._saldo}.")
        else:
            raise ValueError("El monto debe ser positivo.")

    @registrar_movimiento
    def retirar(self, monto):
        if 0 < monto <= self._saldo:
            self._saldo -= monto
            print(f"Se han retirado ${monto}. Saldo actual: ${self._saldo}.")
        else:
            raise ValueError("El monto debe ser mayor que cero y menor o igual al saldo disponible.")

    @registrar_movimiento
    def transferir(self, monto, destinatario):
        if 0 < monto <= self._saldo:
            self._saldo -= monto
            destinatario.depositar(monto)
            print(f"Se han transferido ${monto} a {destinatario.nombre}. Saldo actual: ${self._saldo}.")
        else:
            raise ValueError("El monto debe ser mayor que cero y menor o igual al saldo disponible.")

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}, DNI: {self.dni}, Email: {self.email}, Saldo: ${self.saldo}, CBU: {self.cbu}, Alias: {self.alias}"


# 2.2 Clase Banco
class Banco:
    def __init__(self):
        self.clientes = []

    def agregar_cliente(self, nombre, apellido, dni, email, saldo=0):
        nuevo_cliente = Cliente(nombre, apellido, dni, email)
        nuevo_cliente.saldo = saldo
        self.clientes.append(nuevo_cliente)
        return nuevo_cliente

    def buscar_cliente(self, criterio):
        return [cliente for cliente in self.clientes if criterio in cliente.nombre or criterio == str(cliente.dni)]

    def asignar_alias(self, cliente):
        wordlist = cargar_wordlist(wordlist_txt)
        cliente.asignar_alias(wordlist)

    def generar_resumen(self, cliente):
        return cliente.__str__()

    def __str__(self):
        return f"Banco con {len(self.clientes)} clientes."


# 3. Decorator registrar_movimiento
def registrar_movimiento(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        cliente = args[0]
        monto = args[1]
        accion = func.__name__
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        log_entry = f"{now} - {cliente.nombre} ({cliente.cbu}) [{accion}] ${monto}\n"
        with open("movimientos.log", mode="a") as file:
            file.write(log_entry)
        return resultado

    return wrapper


# 3.2 Manejo de Archivos
def cargar_clientes(archivo):
    clientes = []
    with open(archivo, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            clientes.append(row)
    return clientes


def cargar_wordlist(archivo):
    with open(archivo, mode="r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def limpiar_log(archivo):
    with open(archivo, mode="w") as file:
        pass  # El archivo se abre y se vacía.


# Ejemplo de uso
if __name__ == "__main__":
    # Limpiar el log de movimientos al inicio
    limpiar_log("movimientos.log")

    # Crear banco y cargar clientes
    banco = Banco()
    clientes_data = cargar_clientes(clientes_csv)
    
    for data in clientes_data:
        cliente = banco.agregar_cliente(data['nombre'], data['apellido'], int(data['dni']), data['email'])
        banco.asignar_alias(cliente)

    # Mostrar resumen de un cliente específico
    cliente = banco.buscar_cliente("1")[0]  # Buscar por DNI
    print(banco.generar_resumen(cliente))

    # Realizar operaciones
    cliente.depositar(500)
    cliente.retirar(200)

    # Mostrar información general del banco
    print(banco)
