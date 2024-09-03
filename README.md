
Python para Ciencia de Datos e Inteligencia Artificial - Proyecto Integrador Nº2
Proyecto Integrador Nº2: Sistema Bancario
Objetivo

Desarrollar un sistema bancario en Python que permita gestionar clientes, realizar operaciones bancarias y generar informes, utilizando programación orientada a objetos, manejo de archivos, decorators y expresiones regulares.
Requisitos del Sistema
1. Archivos de Entrada

    clientes.csv: Contiene información de los clientes (nombre, apellido, DNI, email).
    wordlist.txt: Lista de palabras para generar alias de clientes.

2. Clases a Implementar
2.1 Clase Cliente

Atributos:

    Nombre (solo letras y espacios)
    Apellido (solo letras y espacios)
    DNI (número entre 1 y 99.999.999)
    Email (formato válido vía Expresiones Regulares)
    Saldo (inicialmente 0)
    CBU (número aleatorio de 5 dígitos)
    Alias: generado aleatoriamente con el archivo wordlist.txt
        El formato debe ser de 3 palabras aleatorias unidas con .
        Ejemplo: perro.azul.mesa

Métodos:

    depositar(monto)
    retirar(monto)
    transferir(monto, destinatario)
    Getters y setters apropiados
    __str__ para mostrar información del cliente

2.2 Clase Banco

Atributos:

    Lista de clientes

Métodos:

    agregar_cliente(nombre, apellido, dni, email, saldo=0)
    buscar_cliente(criterio) (buscar por nombre parcial o DNI)
    asignar_alias(cliente)
    generar_resumen(cliente)
    __str__ para mostrar información del banco

3. Funcionalidades Adicionales
3.1 Decorator registrar_movimiento

    Registrar operaciones de depósito, retiro y transferencia en un archivo movimientos.log.
    Formato del log:

    dd/mm/yyyy hh:mm - Nombre Cliente (CBU) [acción] $monto

3.2 Manejo de Archivos

    Leer clientes desde clientes.csv
    Leer palabras para alias desde wordlist.txt
    Escribir movimientos en movimientos.log

3.3 Validaciones

    Usar expresiones regulares para validar nombre, apellido, DNI y email.

4. Requerimientos de Implementación

    Utilizar properties para acceder a atributos privados.
    Implementar manejo de excepciones para operaciones inválidas.
    Utilizar list comprehensions donde sea apropiado.

5. Ejemplo de Uso

Implementar un script que demuestre:

    Carga de clientes desde CSV.
    Asignación de alias a todos los clientes.
    Realización de operaciones bancarias (depósito, retiro, transferencia).
    Búsqueda de clientes.
    Generación de resumen para un cliente.
    Mostrar información general del banco.

Criterios de Evaluación

    Correcta implementación de las clases y sus métodos.
    Uso apropiado de decorators, properties y manejo de archivos.
    Validaciones correctas utilizando expresiones regulares.
    Manejo adecuado de excepciones.
    Funcionalidad completa según los requisitos especificados.
    Claridad y organización del código.

Nota

Los archivos clientes.csv y wordlist.txt son proporcionados a continuación. En caso de realizar el script fuera de Colab, asegúrate de que estos archivos estén en el mismo directorio que tu script Python al momento de la ejecución.

clientes.csv https://canvas.instructure.com/courses/9599408/files/268572390?wrap=1

wordlist.txt https://canvas.instructure.com/courses/9599408/files/268572463?wrap=1

Ejemplo de ejecución del Colab adjunto
Salida en movimientos.log

01/09/2024 16:11 - Juan Pérez (54503) ingresó $1000
01/09/2024 16:11 - Juan Pérez (54503) transfirió a María González (73572) $500
01/09/2024 16:11 - María González (73572) retiró $200

Entrega

    Un archivo .ipynb (puede ser una copia de éste 

Links to an external site. Colab) o .py con la solución implementada.