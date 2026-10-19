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
analizador = AnalizadorLexico("texto ```python", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == ["TEXTO", "FIN_LINEA", "EOF"]
assert tokens[0].lexema == "texto ```python"

texto = (
    "> Una cita con `codigo`\n"
    ">> Una cita anidada\n"
    "\n"
    "```python\n"
    "x = 2 ** 3\n"
    "```\n"
    "\n"
    "---"
)
gestor_errores = GestorErrores()
analizador = AnalizadorLexico(texto, gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == [
    "CITA",
    "TEXTO",
    "CODIGO_INLINE",
    "TEXTO_LITERAL",
    "CODIGO_INLINE",
    "FIN_LINEA",
    "CITA",
    "CITA",
    "TEXTO",
    "FIN_LINEA",
    "SALTO_PARRAFO",
    "CERCA_CODIGO",
    "LENGUAJE",
    "FIN_LINEA",
    "TEXTO_LITERAL",
    "CERCA_CODIGO",
    "FIN_LINEA",
    "SALTO_PARRAFO",
    "REGLA_HORIZONTAL",
    "FIN_LINEA",
    "EOF",
]
assert tokens[3].lexema == "codigo"
assert tokens[14].lexema == "x = 2 ** 3"
assert gestor_errores.cantidad() == 0

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("> > doble", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)
assert tipos == ["CITA", "CITA", "TEXTO", "FIN_LINEA", "EOF"]
assert gestor_errores.cantidad() == 0

gestor_errores = GestorErrores()
analizador = AnalizadorLexico(">sin espacio", gestor_errores)
tokens = analizador.tokenizar()
assert tokens[0].tipo == "CITA"
assert tokens[1].lexema == "sin espacio"
assert gestor_errores.cantidad() == 1
assert gestor_errores.errores[0].tipo == "CITA_MAL_FORMADA"
assert gestor_errores.errores[0].fase == "Sintáctico"
assert gestor_errores.errores[0].descripcion == (
    "Cita mal formada en línea 1, columna 1"
)

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("```python\nsin cierre", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)
assert tipos == [
    "CERCA_CODIGO",
    "LENGUAJE",
    "FIN_LINEA",
    "TEXTO_LITERAL",
    "CERCA_CODIGO",
    "FIN_LINEA",
    "EOF",
]
assert tokens[3].lexema == "sin cierre"
assert tokens[4].lexema == ""
assert gestor_errores.cantidad() == 1
assert gestor_errores.errores[0].tipo == "BLOQUE_CODIGO_SIN_CERRAR"
assert gestor_errores.errores[0].fase == "Léxico"

texto = (
    "# Notas **importantes**\n"
    "\n"
    "- Lexico\n"
    "  - AFD\n"
    "    - Estados con *cursiva*\n"
    "- Sintactico"
)
gestor_errores = GestorErrores()
analizador = AnalizadorLexico(texto, gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)

assert tipos == [
    "NUMERAL",
    "TEXTO",
    "NEGRITA",
    "TEXTO",
    "NEGRITA",
    "FIN_LINEA",
    "SALTO_PARRAFO",
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "INDENT",
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "INDENT",
    "VIÑETA",
    "TEXTO",
    "CURSIVA",
    "TEXTO",
    "CURSIVA",
    "FIN_LINEA",
    "DEDENT",
    "DEDENT",
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "EOF",
]

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("- Uno\n    - Dos", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)
assert tipos == [
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "INDENT",
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "DEDENT",
    "EOF",
]
assert gestor_errores.cantidad() == 1
assert gestor_errores.errores[0].tipo == "INDENTACION_INVALIDA"
assert gestor_errores.errores[0].fase == "Sintáctico"
assert gestor_errores.errores[0].descripcion == (
    "Indentación inválida en línea 2, columna 1"
)

gestor_errores = GestorErrores()
analizador = AnalizadorLexico("- Uno\n  - Dos\n\n", gestor_errores)
tokens = analizador.tokenizar()
tipos = []
for token in tokens:
    tipos.append(token.tipo)
assert tipos == [
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "INDENT",
    "VIÑETA",
    "TEXTO",
    "FIN_LINEA",
    "DEDENT",
    "SALTO_PARRAFO",
    "EOF",
]

print("Pruebas léxicas correctas.")
