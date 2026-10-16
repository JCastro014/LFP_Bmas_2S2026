from src.analizador_lexico import AnalizadorLexico
from src.analizador_sintactico import AnalizadorSintactico
from src.gestor_errores import GestorErrores


gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(
    "# Notas **importantes**",
    gestor_errores,
)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert arbol.tipo == "documento"
assert gestor_errores.cantidad() == 0

gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(
    "Esto es **importante",
    gestor_errores,
)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
analizador_sintactico.parsear_documento()
assert gestor_errores.cantidad() == 1
assert gestor_errores.errores[0].tipo == "NEGRITA_SIN_CERRAR"
assert gestor_errores.errores[0].fase == "Léxico"

texto = (
    "# Titulo\n"
    "Primera línea del párrafo.\n"
    "Segunda línea del párrafo.\n"
    "```python\n"
    "x = 2\n"
    "```\n"
    "---"
)
gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(texto, gestor_errores)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert arbol.tipo == "documento"
assert gestor_errores.cantidad() == 0

texto_lista = (
    "# Notas **importantes**\n"
    "\n"
    "- Lexico\n"
    "  - AFD\n"
    "    - Estados con *cursiva*\n"
    "- Sintactico\n"
)
gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(texto_lista, gestor_errores)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert gestor_errores.cantidad() == 0
assert arbol.profundidad_maxima_listas() == 3

texto_cita = (
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
analizador_lexico = AnalizadorLexico(texto_cita, gestor_errores)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert gestor_errores.cantidad() == 0
assert arbol.profundidad_maxima_citas() == 2

archivo = open("ejemplos/ejemplo_valido.md", "r", encoding="utf-8")
texto_ejemplo = archivo.read()
archivo.close()
gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(texto_ejemplo, gestor_errores)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert gestor_errores.cantidad() == 0
assert arbol.profundidad_maxima_listas() == 3
assert arbol.profundidad_maxima_citas() == 2

texto_indentacion_invalida = "- Nivel 0\n    - Salto de nivel\n"
gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(texto_indentacion_invalida, gestor_errores)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert arbol.tipo == "documento"
assert gestor_errores.errores[0].tipo == "INDENTACION_INVALIDA"

gestor_errores = GestorErrores()
analizador_lexico = AnalizadorLexico(">sin espacio", gestor_errores)
tokens = analizador_lexico.tokenizar()
analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
arbol = analizador_sintactico.parsear_documento()
assert arbol.tipo == "documento"
assert gestor_errores.errores[0].tipo == "CITA_MAL_FORMADA"

print("Pruebas sintácticas correctas.")
