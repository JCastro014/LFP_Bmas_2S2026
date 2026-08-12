class Intento:
    def __init__(self, jugador, tablero, solucion, tiempo_segundos, fecha):
        self.jugador = jugador
        self.tablero = tablero
        self.solucion = solucion
        self.tiempo_segundos = tiempo_segundos
        self.fecha = fecha
        self.matriz_solucion = None
        self.validez_porcentaje = None
        self.resuelto_correctamente = False

        self.generar_matriz_solucion()

    def generar_matriz_solucion(self):
        self.matriz_solucion = []
        tamaño = 9
        for i in range(0, len(self.solucion), tamaño):
            fila_texto = self.solucion[i:i + tamaño]
            fila_numeros = []
            for caracter in fila_texto:
                fila_numeros.append(int(caracter))
            self.matriz_solucion.append(fila_numeros)

    def __str__(self):
        return f"Intento de {self.jugador.nombre} {self.jugador.apellido}: Tiempo: {self.tiempo_segundos} segundos, Fecha: {self.fecha}, Validez: {self.validez_porcentaje}%, Resuelto Correctamente: {self.resuelto_correctamente}"