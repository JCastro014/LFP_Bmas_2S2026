def obtener_fila(matriz, numero_fila):
    return matriz[numero_fila]





def obtener_columna(matriz, numero_columna):
    columna = []
    for fila in matriz:
        columna.append(fila[numero_columna])
    return columna
def obtener_caja(matriz, numero_caja):
    fila_inicio = (numero_caja // 3) * 3
    columna_inicio = (numero_caja % 3) * 3
    caja = []
    for f in range(fila_inicio, fila_inicio + 3):
        for c in range(columna_inicio, columna_inicio + 3):
            caja.append(matriz[f][c])
    return caja
def verificar_pistas(tablero, intento):
    matriz_original = tablero.matriz
    matriz_propuesta = intento.matriz_solucion
    for fila in range(9):
        for columna in range(9):
            valor_original = matriz_original[fila][columna]
            valor_propuesto = matriz_propuesta[fila][columna]
            if valor_original != 0:
                if valor_original != valor_propuesto:
                    return False
    return True
def es_grupo_valido(grupo):
    esperado = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    grupo_ordenado = sorted(grupo)
    if grupo_ordenado == esperado:
        return True
    else:
        return False
def validar_intento(tablero, intento):
    grupos_correctos = 0
    matriz = intento.matriz_solucion
    for i in range(9):
        fila = obtener_fila(matriz, i)
        if es_grupo_valido(fila):
            grupos_correctos += 1
    for i in range(9):
        columna = obtener_columna(matriz, i)
        if es_grupo_valido(columna):
            grupos_correctos += 1

    for i in range(9):
        caja = obtener_caja(matriz, i)
        if es_grupo_valido(caja):
            grupos_correctos += 1
    porcentaje = (grupos_correctos / 27) * 100
    intento.validez_porcentaje = porcentaje

    pistas_respetadas = verificar_pistas(tablero, intento)

    if porcentaje == 100 and pistas_respetadas:
        intento.resuelto_correctamente = True
    else:
        intento.resuelto_correctamente = False

    return intento