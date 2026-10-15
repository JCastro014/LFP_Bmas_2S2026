class Error:
    def __init__(self, numero, lexema, tipo, descripcion, linea, columna, fase):
        self.numero = numero
        self.lexema = lexema
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna
        self.fase = fase

    def __str__(self):
        return (
            f"{self.numero:<4} {self.lexema:<15} {self.tipo:<25} "
            f"línea {self.linea}, columna {self.columna}: "
            f"{self.descripcion} ({self.fase})"
        )


class GestorErrores:
    def __init__(self):
        self.errores = []
        self.numero_error = 1

    def agregar(self, lexema, tipo, descripcion, linea, columna, fase):
        error = Error(
            self.numero_error,
            lexema,
            tipo,
            descripcion,
            linea,
            columna,
            fase,
        )
        self.errores.append(error)
        self.numero_error += 1

    def cantidad(self):
        return len(self.errores)

    def hay_errores(self):
        return self.cantidad() > 0

    def imprimir(self):
        for error in self.errores:
            print(error)
