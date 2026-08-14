from Logica.metricas import tiempo_promedio, tasa_de_exito, intentos_por_sudoku
from Logica.metricas import intentos_por_jugador, validez_promedio

def generar_reporte_sudokus(lista_sudokus, lista_intentos):
    html = "<html><head><title>Resumen por Sudoku</title></head><body>"
    html += "<h1>Resumen por Sudoku</h1>"
    html += "<table border='1'>"
    html += "<tr><th>ID</th><th>Dificultad</th><th>Cantidad de Intentos</th><th>Tiempo Promedio</th><th>Tasa de Exito</th></tr>"
    for tablero in lista_sudokus:
        intentos_de_este_sudoku = intentos_por_sudoku(lista_intentos, tablero.id_sudoku)
        cantidad = len(intentos_de_este_sudoku)
        promedio = tiempo_promedio(intentos_de_este_sudoku)
        exito = tasa_de_exito(intentos_de_este_sudoku)
        html += "<tr>"
        html += "<td>" + str(tablero.id_sudoku) + "</td>"
        html += "<td>" + tablero.dificultad + "</td>"
        html += "<td>" + str(cantidad) + "</td>"
        html += "<td>" + str(round(promedio, 2)) + " seg</td>"
        html += "<td>" + str(round(exito, 2)) + "%</td>"
        html += "</tr>"

    html += "</table></body></html>"
    with open("reportes/reporte_sudokus.html", "w") as archivo:
        archivo.write(html)
def generar_reporte_jugadores(lista_jugadores, lista_intentos):
    html = "<html><head><title>Rendimiento por Jugador</title></head><body>"
    html += "<h1>Rendimiento por Jugador</h1>"
    html += "<table border='1'>"
    html += "<tr><th>Carnet</th><th>Nombre</th><th>Nivel</th><th>Tableros Intentados</th><th>Validez Promedio</th><th>Tiempo Promedio</th><th>Resueltos Perfectamente</th></tr>"

    for jugador in lista_jugadores:
        intentos_de_este_jugador = intentos_por_jugador(lista_intentos, jugador.carnet)
        cantidad = len(intentos_de_este_jugador)
        validez = validez_promedio(intentos_de_este_jugador)
        promedio = tiempo_promedio(intentos_de_este_jugador)

        resueltos_perfectos = 0
        for intento in intentos_de_este_jugador:
            if intento.resuelto_correctamente:
                resueltos_perfectos += 1

        nombre_completo = jugador.nombre + " " + jugador.apellido
        html += "<tr>"
        html += "<td>" + str(jugador.carnet) + "</td>"
        html += "<td>" + nombre_completo + "</td>"
        html += "<td>" + jugador.nivel + "</td>"
        html += "<td>" + str(cantidad) + "</td>"
        html += "<td>" + str(round(validez, 2)) + "%</td>"
        html += "<td>" + str(round(promedio, 2)) + " seg</td>"
        html += "<td>" + str(resueltos_perfectos) + "</td>"
        html += "</tr>"
    html += "</table></body></html>"
    with open("reportes/reporte_jugadores.html", "w") as archivo:
        archivo.write(html)
def generar_reporte_top10(lista_intentos):
    intentos_correctos = []
    for intento in lista_intentos:
        if intento.resuelto_correctamente:
            intentos_correctos.append(intento)
    intentos_ordenados = sorted(intentos_correctos, key=lambda i: i.tiempo_segundos)
    top10 = intentos_ordenados[:10]
    html = "<html><head><title>Top 10 Mejores Tiempos</title></head><body>"
    html += "<h1>Top 10 Mejores Tiempos</h1>"
    html += "<table border='1'>"
    html += "<tr><th>Posicion</th><th>Carnet</th><th>Nombre</th><th>Sudoku</th><th>Dificultad</th><th>Tiempo</th></tr>"
    posicion = 1
    for intento in top10:
        nombre_completo = intento.jugador.nombre + " " + intento.jugador.apellido
        html += "<tr>"
        html += "<td>" + str(posicion) + "</td>"
        html += "<td>" + str(intento.jugador.carnet) + "</td>"
        html += "<td>" + nombre_completo + "</td>"
        html += "<td>" + str(intento.tablero.id_sudoku) + "</td>"
        html += "<td>" + intento.tablero.dificultad + "</td>"
        html += "<td>" + str(intento.tiempo_segundos) + " seg</td>"
        html += "</tr>"
        posicion += 1
    html += "</table></body></html>"
    with open("reportes/reporte_top10.html", "w") as archivo:
        archivo.write(html)