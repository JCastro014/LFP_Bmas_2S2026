from src.analizador_lexico import AnalizadorLexico
from src.gestor_errores import GestorErrores


texto = "# Titulo\n\n---\ntexto"
gestor_errores = GestorErrores()
analizador = AnalizadorLexico(texto, gestor_errores)
tokens = analizador.tokenizar()

tipos = []
for token in tokens:
    tipos.append(token.tipo)

tipos_esperados = [
    "NUMERAL",
    "TEXTO",
    "FIN_LINEA",
    "SALTO_PARRAFO",
    "REGLA_HORIZONTAL",
    "FIN_LINEA",
    "TEXTO",
    "FIN_LINEA",
    "EOF",
]

assert tipos == tipos_esperados


gestor_errores = GestorErrores()
analizador = AnalizadorLexico("# Notas **importantes**", gestor_errores)
tokens = analizador.tokenizar()
tipos_y_lexemas = []
for token in tokens:
    tipos_y_lexemas.append((token.tipo, token.lexema))

assert tipos_y_lexemas == [
    ("NUMERAL", "#"),
    ("TEXTO", "Notas "),
    ("NEGRITA", "**"),
    ("TEXTO", "importantes"),
    ("NEGRITA", "**"),
    ("FIN_LINEA", ""),
    ("EOF", ""),
]

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("Esto es **importante", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == ["TEXTO", "TEXTO", "TEXTO", "FIN_LINEA", "EOF"]
assert gestor_errores.cantidad() == 1
error = gestor_errores.errores[0]
assert error.tipo == "NEGRITA_SIN_CERRAR"
assert error.linea == 1
assert error.columna == 9
assert error.descripcion == "Negrita sin cerrar iniciada en línea 1, columna 9"

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("`x = 2 ** 3`", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == [
    "CODIGO_INLINE",
    "TEXTO_LITERAL",
    "CODIGO_INLINE",
    "FIN_LINEA",
    "EOF",
]
assert tokens[1].lexema == "x = 2 ** 3"

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("####### mucho", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == ["TEXTO", "FIN_LINEA", "EOF"]
assert gestor_errores.cantidad() == 1
assert gestor_errores.errores[0].tipo == "ENCABEZADO_INVALIDO"
assert gestor_errores.errores[0].descripcion == (
    "Encabezado inválido en línea 1: máximo 6 niveles"
)

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("```python", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == ["TEXTO", "FIN_LINEA", "EOF"]
assert tokens[0].lexema == "```python"

print("Pruebas léxicas correctas.")
