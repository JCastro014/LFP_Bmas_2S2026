class GeneradorEstadisticas:
    def __init__(self, arbol, nombre_archivo):
        self.arbol = arbol
        self.nombre_archivo = nombre_archivo
        self.total_palabras = 0
        self.total_parrafos = 0
        self.encabezados = [0, 0, 0, 0, 0, 0]
        self.total_listas = 0
        self.total_citas = 0
        self.total_bloques_codigo = 0
        self.total_negritas = 0
        self.total_cursivas = 0
        self.total_codigo_inline = 0

    def generar(self):
        self.total_palabras = 0
        self.total_parrafos = 0
        self.encabezados = [0, 0, 0, 0, 0, 0]
        self.total_listas = 0
        self.total_citas = 0
        self.total_bloques_codigo = 0
        self.total_negritas = 0
        self.total_cursivas = 0
        self.total_codigo_inline = 0

        self._recorrer(self.arbol, False)
        profundidad_listas = self.arbol.profundidad_maxima_listas()
        profundidad_citas = self.arbol.profundidad_maxima_citas()

        html = "<!DOCTYPE html>\n"
        html += '<html lang="es">\n'
        html += "<head>\n"
        html += '<meta charset="utf-8">\n'
        html += "<title>Estadísticas del Documento</title>\n"
        html += "<style>\n"
        html += "body {\n"
        html += "    font-family: Verdana, sans-serif;\n"
        html += "    background: #f4f1ea;\n"
        html += "    color: #222;\n"
        html += "    max-width: 900px;\n"
        html += "    margin: 2em auto;\n"
        html += "    padding: 0 1em;\n"
        html += "}\n"
        html += "h1 {\n"
        html += "    border-bottom: 2px solid #8b3a3a;\n"
        html += "}\n"
        html += "table {\n"
        html += "    border-collapse: collapse;\n"
        html += "    width: 100%;\n"
        html += "}\n"
        html += "th, td {\n"
        html += "    border: 1px solid #8b3a3a;\n"
        html += "    padding: 8px;\n"
        html += "    text-align: left;\n"
        html += "}\n"
        html += "</style>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "<h1>Estadísticas del Documento</h1>\n"
        html += "<p>" + self._escapar(self.nombre_archivo) + "</p>\n"
        html += "<table>\n"
        html += "<tr><th>Dato</th><th>Cantidad</th></tr>\n"
        html += self._fila("Total de palabras", self.total_palabras)
        html += self._fila("Total de párrafos", self.total_parrafos)
        html += self._fila("Listas de primer nivel", self.total_listas)
        html += self._fila("Profundidad máxima de listas", profundidad_listas)
        html += self._fila("Cantidad de citas", self.total_citas)
        html += self._fila("Profundidad máxima de citas", profundidad_citas)
        html += self._fila("Bloques de código", self.total_bloques_codigo)
        html += self._fila("Tramos de negrita", self.total_negritas)
        html += self._fila("Tramos de cursiva", self.total_cursivas)
        html += self._fila("Tramos de código en línea", self.total_codigo_inline)
        html += "</table>\n"
        html += "<h2>Encabezados por nivel</h2>\n"
        html += "<table>\n"
        html += "<tr><th>Nivel</th><th>Cantidad</th></tr>\n"
        nivel = 0
        while nivel < 6:
            html += "<tr><td>H" + str(nivel + 1) + "</td><td>"
            html += str(self.encabezados[nivel]) + "</td></tr>\n"
            nivel += 1
        html += "</table>\n"
        html += "</body>\n</html>\n"
        return html

    def guardar(self, ruta):
        contenido = self.generar()
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def _fila(self, nombre, cantidad):
        return (
            "<tr><td>"
            + nombre
            + "</td><td>"
            + str(cantidad)
            + "</td></tr>\n"
        )

    def _recorrer(self, nodo, dentro_lista):
        if nodo.tipo == "TEXTO":
            self.total_palabras += self._contar_palabras(nodo.lexema)
        elif nodo.tipo == "parrafo":
            self.total_parrafos += 1
        elif nodo.tipo == "encabezado":
            self._contar_encabezado(nodo)
        elif nodo.tipo == "lista":
            if not dentro_lista:
                self.total_listas += 1
        elif nodo.tipo == "cita":
            self.total_citas += 1
        elif nodo.tipo == "bloque_codigo":
            self.total_bloques_codigo += 1
        elif nodo.tipo == "negrita":
            self.total_negritas += 1
        elif nodo.tipo == "cursiva":
            self.total_cursivas += 1
        elif nodo.tipo == "codigo_inline":
            self.total_codigo_inline += 1

        lista_actual = dentro_lista or nodo.tipo == "lista"
        for hijo in nodo.hijos:
            self._recorrer(hijo, lista_actual)

    def _contar_palabras(self, texto):
        palabras = 0
        dentro_palabra = False

        for caracter in texto:
            es_separador = (
                caracter == " "
                or caracter == "\t"
                or caracter == "\n"
                or caracter == "\r"
            )
            if es_separador:
                dentro_palabra = False
            elif not dentro_palabra:
                palabras += 1
                dentro_palabra = True
        return palabras

    def _contar_encabezado(self, nodo):
        cantidad_numerales = 0
        for hijo in nodo.hijos:
            if hijo.tipo == "NUMERAL":
                for caracter in hijo.lexema:
                    if caracter == "#":
                        cantidad_numerales += 1

        if 1 <= cantidad_numerales <= 6:
            self.encabezados[cantidad_numerales - 1] += 1

    def _escapar(self, texto):
        resultado = ""
        for caracter in texto:
            if caracter == "&":
                resultado += "&amp;"
            elif caracter == "<":
                resultado += "&lt;"
            elif caracter == ">":
                resultado += "&gt;"
            elif caracter == '"':
                resultado += "&quot;"
            else:
                resultado += caracter
        return resultado
