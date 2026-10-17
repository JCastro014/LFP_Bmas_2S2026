class GeneradorHTML:
    def __init__(self, arbol, nombre_archivo):
        self.arbol = arbol
        self.nombre_archivo = nombre_archivo
        self.numero_seccion = 0
        self.nivel_cita = 0

    def generar(self):
        self.numero_seccion = 0
        self.nivel_cita = 0
        contenido = self._generar_bloques(self.arbol)
        titulo = self._escapar(self.nombre_archivo)

        html = "<!DOCTYPE html>\n"
        html += '<html lang="es">\n'
        html += "<head>\n"
        html += '<meta charset="utf-8">\n'
        html += "<title>" + titulo + "</title>\n"
        html += "<style>\n"
        html += "body {\n"
        html += "    font-family: Verdana, sans-serif;\n"
        html += "    line-height: 1.6;\n"
        html += "    max-width: 900px;\n"
        html += "    margin: 2em auto;\n"
        html += "    padding: 0 1em;\n"
        html += "    background: #f4f1ea;\n"
        html += "    color: #222;\n"
        html += "}\n"
        html += "h1 {\n"
        html += "    border-bottom: 2px solid #8b3a3a;\n"
        html += "}\n"
        html += "pre {\n"
        html += "    background: #2b2b2b;\n"
        html += "    color: #eee;\n"
        html += "    font-family: Consolas, monospace;\n"
        html += "    padding: 10px;\n"
        html += "    overflow-x: auto;\n"
        html += "}\n"
        html += "blockquote {\n"
        html += "    border-left: 3px solid #8b3a3a;\n"
        html += "    margin-left: 0;\n"
        html += "    padding-left: 1em;\n"
        html += "    color: #555;\n"
        html += "}\n"
        html += ".estado {\n"
        html += "    background: #d8f3dc;\n"
        html += "    color: #1b5e20;\n"
        html += "    padding: 10px;\n"
        html += "}\n"
        html += "</style>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += '<p class="estado">Análisis completado sin errores</p>\n'
        html += contenido
        html += "\n</body>\n</html>\n"
        return html

    def guardar(self, ruta):
        contenido = self.generar()
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def _escapar(self, texto):
        resultado = ""
        for caracter in texto:
            if caracter == "&":
                resultado += "&amp;"
            elif caracter == "<":
                resultado += "&lt;"
            elif caracter == ">":
                resultado += "&gt;"
            else:
                resultado += caracter
        return resultado

    def _hijo_tipo(self, nodo, tipo):
        for hijo in nodo.hijos:
            if hijo.tipo == tipo:
                return hijo
        return None

    def _generar_bloques(self, nodo):
        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "bloques":
                contenido += self._generar_bloques(hijo)
            elif hijo.tipo == "bloque":
                contenido += self._generar_bloque(hijo)
        return contenido

    def _generar_bloque(self, nodo):
        for hijo in nodo.hijos:
            if hijo.tipo == "encabezado":
                return self._generar_encabezado(hijo)
            if hijo.tipo == "parrafo":
                return self._generar_parrafo(hijo)
            if hijo.tipo == "lista":
                return self._generar_lista(hijo)
            if hijo.tipo == "cita":
                return self._generar_cita(hijo)
            if hijo.tipo == "bloque_codigo":
                return self._generar_bloque_codigo(hijo)
            if hijo.tipo == "regla":
                return self._generar_regla(hijo)
        return ""

    def _generar_encabezado(self, nodo):
        numeral = self._hijo_tipo(nodo, "NUMERAL")
        linea = self._hijo_tipo(nodo, "en_linea")
        nivel = 0
        for caracter in numeral.lexema:
            if caracter == "#":
                nivel += 1

        self.numero_seccion += 1
        texto = self._generar_en_linea(linea)
        etiqueta = "h" + str(nivel)
        identificador = ' id="seccion-' + str(self.numero_seccion) + '"'
        return (
            "<"
            + etiqueta
            + identificador
            + ">"
            + texto
            + "</"
            + etiqueta
            + ">\n"
        )

    def _generar_regla(self, nodo):
        return "<hr>\n"

    def _generar_parrafo(self, nodo):
        linea = self._hijo_tipo(nodo, "linea_texto")
        resto = self._hijo_tipo(nodo, "parrafo_resto")
        texto = self._generar_linea_texto(linea)
        texto += self._generar_parrafo_resto(resto)
        return "<p>" + texto + "</p>\n"

    def _generar_parrafo_resto(self, nodo):
        if nodo is None:
            return ""

        linea = self._hijo_tipo(nodo, "linea_texto")
        resto = self._hijo_tipo(nodo, "parrafo_resto")
        if linea is None:
            return ""
        return (
            " "
            + self._generar_linea_texto(linea)
            + self._generar_parrafo_resto(resto)
        )

    def _generar_linea_texto(self, nodo):
        elemento = self._hijo_tipo(nodo, "elemento")
        linea = self._hijo_tipo(nodo, "en_linea")
        texto = ""
        if elemento is not None:
            texto += self._generar_elemento(elemento)
        texto += self._generar_en_linea(linea)
        return texto

    def _generar_en_linea(self, nodo):
        if nodo is None:
            return ""

        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "elemento":
                contenido += self._generar_elemento(hijo)
            elif hijo.tipo == "en_linea":
                contenido += self._generar_en_linea(hijo)
        return contenido

    def _generar_elemento(self, nodo):
        for hijo in nodo.hijos:
            if hijo.tipo == "negrita":
                return self._generar_negrita(hijo)
            if hijo.tipo == "cursiva":
                return self._generar_cursiva(hijo)
            if hijo.tipo == "codigo_inline":
                return self._generar_codigo_inline(hijo)
            if hijo.tipo == "TEXTO":
                return self._escapar(hijo.lexema)
        return ""

    def _generar_negrita(self, nodo):
        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "en_negrita":
                contenido += self._generar_en_negrita(hijo)
        return "<strong>" + contenido + "</strong>"

    def _generar_en_negrita(self, nodo):
        return self._generar_contenido_inline(nodo)

    def _generar_cursiva(self, nodo):
        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "en_cursiva":
                contenido += self._generar_en_cursiva(hijo)
        return "<em>" + contenido + "</em>"

    def _generar_en_cursiva(self, nodo):
        return self._generar_contenido_inline(nodo)

    def _generar_codigo_inline(self, nodo):
        literal = self._hijo_tipo(nodo, "TEXTO_LITERAL")
        texto = ""
        if literal is not None:
            texto = self._escapar(literal.lexema)
        return "<code>" + texto + "</code>"

    def _generar_elem_neg(self, nodo):
        return self._generar_contenido_inline(nodo)

    def _generar_elem_curs(self, nodo):
        return self._generar_contenido_inline(nodo)

    def _generar_contenido_inline(self, nodo):
        contenido = ""
        for hijo in nodo.hijos:
            contenido += self._generar_nodo_inline(hijo)
        return contenido

    def _generar_nodo_inline(self, nodo):
        if nodo.tipo == "elemento":
            return self._generar_elemento(nodo)
        if nodo.tipo == "negrita":
            return self._generar_negrita(nodo)
        if nodo.tipo == "en_negrita":
            return self._generar_en_negrita(nodo)
        if nodo.tipo == "elem_neg":
            return self._generar_elem_neg(nodo)
        if nodo.tipo == "cursiva":
            return self._generar_cursiva(nodo)
        if nodo.tipo == "en_cursiva":
            return self._generar_en_cursiva(nodo)
        if nodo.tipo == "elem_curs":
            return self._generar_elem_curs(nodo)
        if nodo.tipo == "codigo_inline":
            return self._generar_codigo_inline(nodo)
        if nodo.tipo == "TEXTO" or nodo.tipo == "TEXTO_LITERAL":
            return self._escapar(nodo.lexema)
        return self._generar_contenido_inline(nodo)

    def _generar_lista(self, nodo):
        primer_item = self._hijo_tipo(nodo, "item_lista")
        resto = self._hijo_tipo(nodo, "lista_resto")
        contenido = ""
        if primer_item is not None:
            contenido += self._generar_item_lista(primer_item)
        contenido += self._generar_lista_resto(resto)
        return "<ul>" + contenido + "</ul>\n"

    def _generar_lista_resto(self, nodo):
        if nodo is None:
            return ""

        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "item_lista":
                contenido += self._generar_item_lista(hijo)
            elif hijo.tipo == "lista_resto":
                contenido += self._generar_lista_resto(hijo)
        return contenido

    def _generar_item_lista(self, nodo):
        linea = self._hijo_tipo(nodo, "en_linea")
        sublista = self._hijo_tipo(nodo, "sublista_opt")
        contenido = self._generar_en_linea(linea)
        contenido += self._generar_sublista_opt(sublista)
        return "<li>" + contenido + "</li>"

    def _generar_sublista_opt(self, nodo):
        if nodo is None:
            return ""

        lista = self._hijo_tipo(nodo, "lista")
        if lista is None:
            return ""
        return self._generar_lista(lista)

    def _generar_cita(self, nodo):
        self.nivel_cita = 0
        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "linea_cita":
                contenido += self._generar_linea_cita(hijo)
            elif hijo.tipo == "cita_resto":
                contenido += self._generar_cita_resto(hijo)

        while self.nivel_cita > 0:
            contenido += "</blockquote>"
            self.nivel_cita -= 1
        return contenido + "\n"

    def _generar_cita_resto(self, nodo):
        contenido = ""
        for hijo in nodo.hijos:
            if hijo.tipo == "linea_cita":
                contenido += self._generar_linea_cita(hijo)
            elif hijo.tipo == "cita_resto":
                contenido += self._generar_cita_resto(hijo)
        return contenido

    def _generar_linea_cita(self, nodo):
        nivel = self._contar_citas(nodo)
        contenido = ""

        # De 1 a 2 niveles se abre otro bloque; al volver a 1 se cierra.
        while self.nivel_cita < nivel:
            contenido += "<blockquote>"
            self.nivel_cita += 1
        while self.nivel_cita > nivel:
            contenido += "</blockquote>"
            self.nivel_cita -= 1

        cuerpo = self._hijo_tipo(nodo, "cuerpo_cita")
        contenido += "<p>" + self._generar_cuerpo_cita(cuerpo) + "</p>"
        return contenido

    def _generar_cuerpo_cita(self, nodo):
        return self._generar_contenido_inline(nodo)

    def _contar_citas(self, nodo):
        cantidad = 0
        if nodo.tipo == "CITA":
            cantidad = 1
        for hijo in nodo.hijos:
            cantidad += self._contar_citas(hijo)
        return cantidad

    def _generar_bloque_codigo(self, nodo):
        lenguaje = ""
        opcion = self._hijo_tipo(nodo, "lenguaje_opt")
        if opcion is not None:
            token_lenguaje = self._hijo_tipo(opcion, "LENGUAJE")
            if token_lenguaje is not None:
                lenguaje = self._escapar(token_lenguaje.lexema)

        clase = ""
        if lenguaje != "":
            clase = ' class="language-' + lenguaje + '"'

        contenido_cod = self._hijo_tipo(nodo, "contenido_cod")
        contenido = self._generar_contenido_cod(contenido_cod)
        return "<pre><code" + clase + ">" + contenido + "</code></pre>\n"

    def _generar_contenido_cod(self, nodo):
        if nodo is None:
            return ""
        literal = self._hijo_tipo(nodo, "TEXTO_LITERAL")
        if literal is None:
            return ""
        return self._escapar(literal.lexema)
