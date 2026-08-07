class Tablero:
    def __init__(self, id, dificultad, cadena):
        self.id = id
        self.dificultad = dificultad
        self.tablero_original = cadena
        self.matriz = None

    def generar_matriz(self):
        
        self.matriz = []
        tamaño = 9
        for i in range(0, len(self.tablero_original), tamaño):
            fila_texto = self.tablero_original[i:i + tamaño]
            fila_numeros = []
            for caracter in fila_texto:
                fila_numeros.append(int(caracter))
            self.matriz.append(fila_numeros)

    def obtener_fila(self, numero_fila):
        
        return self.matriz[numero_fila]

    def obtener_columna(self, numero_columna):
    
        columna = []
        for fila in self.matriz:
            columna.append(fila[numero_columna])
        return columna

    def obtener_caja(self, numero_caja):
        fila_inicio = (numero_caja // 3) * 3
        columna_inicio = (numero_caja % 3) * 3

        caja = []
        for f in range(fila_inicio, fila_inicio + 3):
            for c in range(columna_inicio, columna_inicio + 3):
                caja.append(self.matriz[f][c])
        return caja

    def mostrar_tablero(self):
        for fila in self.matriz:
            print(fila)