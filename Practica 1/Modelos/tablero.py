class Tablero:
    def __init__(self, id, dificultad, cadena):
        self.id = id
        self.dificultad = dificultad
        self.cadena = cadena
        self.tablero_original = cadena
        self.matriz = None