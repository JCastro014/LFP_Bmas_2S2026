from Modelos.tablero import Tablero
from Modelos.jugador import Jugador
from Modelos.intento import Intento
def cargar_sudokus(ruta_archivo):
    sudokus = []
    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                if linea.strip():
                    linea_limpia = linea.strip()
                    partes = linea_limpia.split(',')
                    nuevo_tablero = Tablero(partes[0], partes[1], partes[2])
                    sudokus.append(nuevo_tablero)
    except FileNotFoundError:
        print("Error: no se encontro el archivo " + ruta_archivo)
    except Exception as error:
        print("Error inesperado al leer el archivo: " + str(error))

    return sudokus
def cargar_jugadores(ruta_archivo):
    jugadores = []
    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                if linea.strip():
                    linea_limpia = linea.strip()
                    partes = linea_limpia.split(',')
                    nuevo_jugador = Jugador(partes[0], partes[1], partes[2], partes[3])
                    jugadores.append(nuevo_jugador)
    except FileNotFoundError:
        print("Error: no se encontro el archivo " + ruta_archivo)
    except Exception as error:
        print("Error inesperado al leer el archivo: " + str(error))

    return jugadores
def cargar_intentos(ruta_archivo, lista_jugadores, lista_sudokus):
    intentos = []
    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                if linea.strip():
                    linea_limpia = linea.strip()
                    partes = linea_limpia.split(',')
                    carnet_buscado = int(partes[0])
                    id_sudoku_buscado = int(partes[1])
                    jugador_encontrado = None
                    for jugador in lista_jugadores:
                        if jugador.carnet == carnet_buscado:
                            jugador_encontrado = jugador
                    tablero_encontrado = None
                    for tablero in lista_sudokus:
                        if tablero.id_sudoku == id_sudoku_buscado:
                            tablero_encontrado = tablero
                    if jugador_encontrado is not None and tablero_encontrado is not None:
                        nuevo_intento = Intento(
                            jugador_encontrado,
                            tablero_encontrado,
                            partes[2],
                            partes[3],
                            partes[4]
                        )
                        intentos.append(nuevo_intento)
    except FileNotFoundError:
        print("Error: no se encontro el archivo " + ruta_archivo)
    except Exception as error:
        print("Error inesperado al leer el archivo: " + str(error))
    return intentos