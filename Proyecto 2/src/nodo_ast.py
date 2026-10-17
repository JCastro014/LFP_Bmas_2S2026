class NodoAST:
    def __init__(self, tipo, lexema="", linea=0, columna=0):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def profundidad_maxima_listas(self, nivel=0):
        if self.tipo == "lista":
            nivel = nivel + 1

        profundidad = nivel
        for hijo in self.hijos:
            profundidad_hijo = hijo.profundidad_maxima_listas(nivel)
            if profundidad_hijo > profundidad:
                profundidad = profundidad_hijo
        return profundidad

    def profundidad_maxima_citas(self):
        if self.tipo == "linea_cita":
            return self._contar_tokens("CITA")

        profundidad = 0
        for hijo in self.hijos:
            profundidad_hijo = hijo.profundidad_maxima_citas()
            if profundidad_hijo > profundidad:
                profundidad = profundidad_hijo
        return profundidad

    def _contar_tokens(self, tipo):
        cantidad = 0
        if self.tipo == tipo:
            cantidad = 1

        for hijo in self.hijos:
            cantidad = cantidad + hijo._contar_tokens(tipo)
        return cantidad

    def imprimir(self, nivel=0):
        sangria = "  " * nivel
        texto = sangria + self.tipo
        if self.lexema != "":
            texto = texto + ": " + self.lexema
        if self.linea > 0:
            texto = texto + " (" + str(self.linea) + ", " + str(self.columna) + ")"
        print(texto)

        for hijo in self.hijos:
            hijo.imprimir(nivel + 1)

    def texto_arbol(self, nivel=0):
        sangria = "  " * nivel
        texto = sangria + self.tipo
        if self.lexema != "":
            texto = texto + ": " + self.lexema
        if self.linea > 0:
            texto = texto + " (" + str(self.linea) + ", " + str(self.columna) + ")"

        for hijo in self.hijos:
            texto += "\n" + hijo.texto_arbol(nivel + 1)
        return texto
