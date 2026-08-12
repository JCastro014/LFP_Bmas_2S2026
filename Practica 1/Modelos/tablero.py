class Tablero:
    def __init__(self, id_sudoku, dificultad, cadena):
        self.id_sudoku = int(id_sudoku)
        self.dificultad = dificultad
        self.tablero_original = cadena
        self.matriz = None
        self.generar_matriz()

    def generar_matriz(self):
        self.matriz = []
        tamano = 9
        for i in range(0, len(self.tablero_original), tamano):
            fila_texto = self.tablero_original[i:i + tamano]
            fila_numeros = []
            for caracter in fila_texto:
                fila_numeros.append(int(caracter))
            self.matriz.append(fila_numeros)

    def mostrar_tablero(self):
        for fila in self.matriz:
            print(fila)