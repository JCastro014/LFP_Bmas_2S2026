from .error_lexico import ErrorLexico


class GestorErrores:
    def __init__(self):
        self.errores = []
        self.numero_error = 1

    def agregar(self, lexema, tipo, descripcion, linea, columna):
        error = ErrorLexico(
            self.numero_error,
            lexema,
            tipo,
            descripcion,
            linea,
            columna,
        )
        self.errores.append(error)
        self.numero_error += 1

    def cantidad(self):
        return len(self.errores)
