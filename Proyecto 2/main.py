import os
import sys

from src.analizador_lexico import AnalizadorLexico
from src.gestor_errores import GestorErrores


def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()


def imprimir_tokens(tokens):
    print("No.  Lexema                            Tipo                 Línea Columna")
    print("-" * 78)

    for token in tokens:
        lexema = token.lexema
        if token.tipo == "FIN_LINEA":
            lexema = "(fin de línea)"
        elif token.tipo == "SALTO_PARRAFO":
            lexema = "(salto de párrafo)"
        elif token.tipo == "EOF":
            lexema = "(fin de archivo)"

        print(
            f"{token.numero:<4} {lexema:<34} {token.tipo:<20} "
            f"{token.linea:<6} {token.columna:<7}"
        )


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py archivo.md")
        return 1

    ruta_archivo = sys.argv[1]
    if not os.path.exists(ruta_archivo):
        print("No existe el archivo:", ruta_archivo)
        return 1

    try:
        contenido = leer_archivo(ruta_archivo)
    except OSError as error:
        print("No se pudo leer el archivo:", error)
        return 1

    gestor_errores = GestorErrores()
    analizador = AnalizadorLexico(contenido, gestor_errores)
    tokens = analizador.tokenizar()
    imprimir_tokens(tokens)
    return 0


if __name__ == "__main__":
    sys.exit(main())