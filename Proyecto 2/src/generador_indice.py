class GeneradorIndice:
    def __init__(self, arbol, nombre_archivo):
        self.arbol = arbol
        self.nombre_archivo = nombre_archivo
        self.encabezados = []

    def generar(self):
        self.encabezados = []
        self._buscar_encabezados(self.arbol)

        html = "<!DOCTYPE html>\n"
        html += '<html lang="es">\n'
        html += "<head>\n"
        html += '<meta charset="utf-8">\n'
        html += "<title>Índice del Documento</title>\n"
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
        html += "a {\n"
        html += "    color: #8b3a3a;\n"
        html += "}\n"
        html += "</style>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "<h1>Tabla de contenido</h1>\n"
        html += "<p>" + self._escapar(self.nombre_archivo) + "</p>\n"

        if len(self.encabezados) == 0:
            html += "<p>El documento no tiene encabezados</p>\n"
        else:
            html += "<ul>\n"
            numero = 1
            for encabezado in self.encabezados:
                margen = (encabezado["nivel"] - 1) * 20
                texto = self._escapar(encabezado["texto"])
                html += (
                    '<li style="margin-left: '
                    + str(margen)
                    + 'px"><a href="reporte1_documento.html#seccion-'
                    + str(numero)
                    + '">'
                    + texto
                    + "</a></li>\n"
                )
                numero += 1
            html += "</ul>\n"

        html += "</body>\n</html>\n"
        return html

    def guardar(self, ruta):
        contenido = self.generar()
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def _buscar_encabezados(self, nodo):
        if nodo.tipo == "encabezado":
            self._agregar_encabezado(nodo)

        for hijo in nodo.hijos:
            self._buscar_encabezados(hijo)

    def _agregar_encabezado(self, nodo):
        nivel = 0
        texto = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "NUMERAL":
                for caracter in hijo.lexema:
                    if caracter == "#":
                        nivel += 1
            elif hijo.tipo == "en_linea":
                texto += self._texto_encabezado(hijo)

        self.encabezados.append({"nivel": nivel, "texto": texto})

    def _texto_encabezado(self, nodo):
        texto = ""
        if nodo.tipo == "TEXTO" or nodo.tipo == "TEXTO_LITERAL":
            return nodo.lexema

        for hijo in nodo.hijos:
            texto += self._texto_encabezado(hijo)
        return texto

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
