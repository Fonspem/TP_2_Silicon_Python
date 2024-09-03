import re
import csv
import random
import datetime
import functools


def registrar_movimiento(func): ...


class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: int, email: str):
        self._nombre: str = nombre
        self._apellido: str = apellido
        self._dni: int = dni
        self._email: str = email
        self._saldo: int = 0
        self._cbu: int = random.randint(10000, 99999)
        self._alias: str = self.generar_alias()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not re.match(r"^[A-Za-z\s]+$", valor):
            raise ValueError("El NOMBRE solo puede contener letras y espacios.")
        self._nombre = valor

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        if not re.match(r"^[A-Za-z\s]+$", valor):
            raise ValueError("El Apellido solo puede contener letras y espacios.")
        self._apellido = valor

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, valor):
        if not (1 <= valor <= 99_999_999):
            raise ValueError("El DNI debe ser un número entre 1 y 99.999.999.")
        self._dni = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", valor):
            raise ValueError("El formato de email es inválido.")
        self._email = valor

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    @property
    def cbu(self):
        return self._cbu

    @property
    def alias(self):
        return self._alias

    # METODOS-------------------------------------------------------------------

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("Solo se pueden depositar montos positivos.")
        self.saldo += monto

    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto para retirar debe ser mayor que 0.")
        if monto > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= monto

    def transferir(self, monto, destinatario):
        if not isinstance(destinatario, Cliente):
            raise ValueError("El destinatario debe ser un Cliente.")
        self.retirar(monto)
        destinatario.depositar(monto)

    def __str__(self):
        return (
            f"Cliente: {self.apellido} {self.nombre}\n"
            f"DNI: {self.dni}\n"
            f"Email: {self.email}\n"
            f"Saldo: ${self.saldo}\n"
            f"CBU: {self.cbu}\n"
            f"Alias: {self.alias}"
        )

    def generar_alias(self):
        with open("wordlist.txt", "r") as file:
            palabras = file.read().splitlines()
        alias = ".".join(random.sample(palabras, 3))
        self._alias = alias
        return alias


class Banco: ...


# Ejemplo de uso
banco = Banco()

# Cargar clientes desde CSV
with open("clientes.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        banco.agregar_cliente(row["nombre"], row["apellido"], row["dni"], row["email"])

# Asignar alias a todos los clientes
for cliente in banco.clientes:
    banco.asignar_alias(cliente)

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
