class Token:
    def __init__(self, numero, lexema, tipo, linea, columna):
        self.numero = numero
        self.lexema = lexema
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"{self.numero:<4} {self.lexema:<35} {self.tipo:<20} {self.linea:<5} {self.columna:<5}"
