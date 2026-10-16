import os
import sys

from src.analizador_lexico import AnalizadorLexico
from src.analizador_sintactico import AnalizadorSintactico
from src.gestor_errores import GestorErrores


def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()


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
    analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
    arbol = analizador_sintactico.parsear_documento()

    print("Árbol sintáctico:")
    arbol.imprimir(0)
    print("\nErrores:")
    if gestor_errores.hay_errores():
        gestor_errores.imprimir()
    else:
        print("No se encontraron errores.")

    return 0


if __name__ == "__main__":
    sys.exit(main())