class NodoAST:
    def __init__(self, tipo, lexema="", linea=0, columna=0):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

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
