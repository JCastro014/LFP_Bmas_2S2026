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

print("Pruebas sintácticas correctas.")
