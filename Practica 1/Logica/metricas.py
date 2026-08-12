def tiempo_promedio(lista_intentos):
    if len(lista_intentos) == 0:
        return 0
    suma_tiempos = 0
    for intento in lista_intentos:
        suma_tiempos += intento.tiempo_segundos
    promedio = suma_tiempos / len(lista_intentos)
    return promedio
def validez_promedio(lista_intentos):
    if len(lista_intentos) == 0:
        return 0
    suma_validez = 0
    for intento in lista_intentos:
        suma_validez += intento.validez_porcentaje
    promedio = suma_validez / len(lista_intentos)
    return promedio
def tasa_de_exito(lista_intentos):
    if len(lista_intentos) == 0:
        return 0
    resueltos_correctamente = 0
    for intento in lista_intentos:
        if intento.resuelto_correctamente:
            resueltos_correctamente += 1
    tasa = (resueltos_correctamente / len(lista_intentos)) * 100
    return tasa
def intentos_por_sudoku(lista_intentos, id_sudoku):
    resultado = []
    for intento in lista_intentos:
        if intento.tablero.id_sudoku == id_sudoku:
            resultado.append(intento)
    return resultado
def intentos_por_jugador(lista_intentos, carnet):
    resultado = []
    for intento in lista_intentos:
        if intento.jugador.carnet == carnet:
            resultado.append(intento)
    return resultado