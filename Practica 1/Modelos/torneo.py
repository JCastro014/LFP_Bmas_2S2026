from io_archivos.lector import cargar_sudokus, cargar_jugadores, cargar_intentos
class Torneo:
    def __init__(self):
        self.sudokus = []
        self.jugadores = []
        self.intentos = []
    def cargar_datos_sudokus(self, ruta_archivo):
        self.sudokus = cargar_sudokus(ruta_archivo)
    def cargar_datos_jugadores(self, ruta_archivo):
        self.jugadores = cargar_jugadores(ruta_archivo)
    def cargar_datos_intentos(self, ruta_archivo):
        self.intentos = cargar_intentos(ruta_archivo, self.jugadores, self.sudokus)