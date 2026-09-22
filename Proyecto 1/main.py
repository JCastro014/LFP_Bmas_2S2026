import sys
import tkinter as tk
from pathlib import Path
from horario_script import AnalizadorLexico
from horario_script.gui import VentanaHorarioScript
from horario_script.detector_choques import extraer_clases, detectar_choques
from horario_script.generador_reportes import GeneradorReportes





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
def imprimir_choques(tokens):
	clases = extraer_clases(tokens)
	choques = detectar_choques(clases)
	print(f"\nCHOQUES DE HORARIO: {len(choques)}")
	for choque in choques:
		print(
			f"  {choque['clase1']['curso']} vs {choque['clase2']['curso']} "
			f"- mismo {choque['motivo']}, {choque['clase1']['dia']}"
		)
def analizar_desde_consola(argumentos):
	carpeta_actual = Path(__file__).parent
	ruta = Path(argumentos[0]) if len(argumentos) > 0 else carpeta_actual / "datos" / "horario_valido.hor"
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
	imprimir_choques(tokens)
	return 0
def iniciar_gui():
	raiz = tk.Tk()
	VentanaHorarioScript(raiz)
	raiz.mainloop()
	return 0
def generar_reportes(tokens):
    generador = GeneradorReportes(tokens)
    generador.generar_reporte_horario("reporte_horario.html")
    generador.generar_reporte_carga("reporte_carga.html")
    print("\nReportes generados: reporte_horario.html, reporte_carga.html")
def main():
	argumentos = sys.argv[1:]
	if len(argumentos) > 0 and argumentos[0] == "--consola":
		return analizar_desde_consola(argumentos[1:])
	return iniciar_gui()
if __name__ == "__main__":
	raise SystemExit(main())
