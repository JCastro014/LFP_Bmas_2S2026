def cargar_sudokus(ruta_archivo):
    sudokus = []
    with open(ruta_archivo, "r") as archivo:
        for linea in archivo:
            if linea.strip():  # Verifica si la línea no está vacía
                linea_limpia = linea.strip()
                partes = linea_limpia.split(',')
                nuevoTablero = Tablero(partes[0], partes[1], partes[2])
                sudokus.append(nuevoTablero)
        return sudokus
    