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
print("Pruebas léxicas correctas.")
