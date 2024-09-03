# Estructura de menu dict[str,dict[str,[tuple[str,float]]]]
menu = {
    "bebidas": {
        "latte": ("Café con leche espumosa", 3.5),
        "submarino": ("Chocolate caliente con una barra de chocolate", 3.0),
        "capuchino": ("Café con espuma de leche y canela", 3.75),
        "espresso": ("Café concentrado y fuerte", 2.25),
    },
    "comidas": {
        "muffin": ("Muffin de arándanos", 1.75),
        "medialuna": ("Medialuna dulce", 1.0),
        "tostado": ("Tostado de jamón y queso", 3.5),
        "chipitas": ("Pequeños panes de queso", 2.0),
    },
}

import os


def limpiar_consola():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")  # para linux


def mostrar_menu() -> None:
    for tipo in menu:
        print(
            f"\t{tipo.upper():<15} Precio",
            end="\n",
        )
        for alimento in menu[tipo]:
            print(
                f"{alimento.upper():<25} {(menu[tipo][alimento][1]):<6}",
                sep="",
                end="",
            )
            print(f" {menu[tipo][alimento][0]}")
        print(end="\n")


def mostrar_pedido(pedido: dict) -> None:
    if len(pedido) == 0:
        print("Tu pedido actual está vacío")
        return
    print("Tu pedido actual:\n")
    print("Nombre       Cantidad      Precio")
    precio: float = 0
    total: float = 0
    for elemento in pedido:
        for tipo in menu:
            if elemento in menu[tipo]:
                precio = pedido[elemento] * menu[tipo][elemento][1]
                break
        print(f"{elemento:<15} {pedido[elemento]:>5}{precio:>12}")
        total += precio
    print(f"\nTOTAL:{total:>27}")


def realizar_pedido() -> dict:
    pedido = {}
    while True:
        limpiar_consola()
        mostrar_menu()  # muestro el menu porque es mas cómodo
        mostrar_pedido(pedido)
        try:
            entrada: str = input(
                'Seleccione nombre del item o "Salir" para completar pedido): '
            ).lower()
            if entrada == "salir":
                return pedido
            comida: str = ""
            precio: float = 0
            for tipo in menu:
                if entrada in menu[tipo]:
                    comida = entrada
                    precio = menu[tipo][entrada][1]
                    break
            if comida == "":
                raise Exception("Item no encontrado")
            while True:
                try:
                    cantidad: int = int(
                        input(f"Ingrese cuanto/s {comida.upper()}, {precio}$ c/u : ")
                    )
                    if cantidad != 0:
                        pedido.update({comida: cantidad})
                    break
                except:
                    print("Reintente o 0 para cancelar orden")
        except Exception as error:
            input(f"{error}. Enter para continuar")


def generar_recibo(pedido) -> None:
    with open("recibo.txt", "w") as archivo:  # abrir archivo escritura
        archivo.write("Tu pedido actual:\n")
        archivo.write("Nombre       Cantidad      Precio\n")
        precio: float = 0
        total: float = 0
        for elemento in pedido:  # misma estructura que el mostrar recibo
            for tipo in menu:
                if elemento in menu[tipo]:
                    precio = pedido[elemento] * menu[tipo][elemento][1]
                    break
            archivo.write(f"{elemento:<15} {pedido[elemento]:>5}{precio:>12}\n")
            total += precio
        archivo.write(f"\nTOTAL:{total:>27}")

    with open("recibo.txt", "r") as archivo:  # abrir archivo lectura
        print(archivo.read())


def inicio() -> None:
    pedido: dict = {}
    while True:
        print("Bienvenido a Code & Coffee")
        print("1. Mostrar Menú")
        print("2. Realizar Pedido")
        print("3. Salir")
        try:
            match int(input("Seleccione una opción: ")):
                case 1:
                    limpiar_consola()
                    mostrar_menu()
                case 2:
                    limpiar_consola()
                    pedido = realizar_pedido()
                case 3:
                    limpiar_consola()
                    generar_recibo(pedido)
                    break
                case _:
                    raise ValueError
        except:
            print("Opción no válida. Intente nuevamente.")


inicio()
