class ErrorLexico:
    def __init__(self, numero, lexema, tipo, descripcion, linea, columna):
        self.numero = numero
        self.lexema = lexema
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return (
            f"{self.numero:<4} {self.lexema:<15} {self.tipo:<25} "
            f"linea {self.linea}, columna {self.columna}: {self.descripcion}"
        )
