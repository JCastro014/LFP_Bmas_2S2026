import sys
from pathlib import Path

from horario_script import AnalizadorLexico


def leer_archivo(ruta):
	with open(ruta, "r", encoding="utf-8") as archivo:
		return archivo.read()


def imprimir_resultados(tokens, errores):
	print("\nTOKENS")
	print("No.  Lexema                             Tipo                 Linea Col")
	print("-" * 80)
	for token in tokens:
		print(token)

	print("\nERRORES LEXICOS")
	if len(errores) == 0:
		print("No se encontraron errores.")
	else:
		for error in errores:
			print(error)

	print(f"\nTotal de tokens: {len(tokens)}")
	print(f"Total de errores: {len(errores)}")


def main():
	carpeta_actual = Path(__file__).parent
	ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else carpeta_actual / "datos" / "horario_valido.hor"

	if not ruta.is_absolute() and not ruta.exists():
		ruta = carpeta_actual / ruta

	if not ruta.exists():
		print(f"No existe el archivo: {ruta}")
		return 1

	try:
		texto = leer_archivo(ruta)
	except OSError as error:
		print(f"No se pudo leer el archivo: {error}")
		return 1

	analizador = AnalizadorLexico(texto)
	tokens = analizador.analizar()
	imprimir_resultados(tokens, analizador.errores)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
