from src.analizador_lexico import AnalizadorLexico
from src.analizador_sintactico import AnalizadorSintactico
from src.exportador_dot import generar_dot
from src.generador_estadisticas import GeneradorEstadisticas
from src.generador_html import GeneradorHTML
from src.generador_indice import GeneradorIndice
from src.gestor_errores import GestorErrores


def analizar(texto):
    gestor_errores = GestorErrores()
    analizador_lexico = AnalizadorLexico(texto, gestor_errores)
    tokens = analizador_lexico.tokenizar()
    analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
    arbol = analizador_sintactico.parsear_documento()
    assert gestor_errores.cantidad() == 0
    return arbol


archivo = open("ejemplos/ejemplo_valido.md", "r", encoding="utf-8")
texto_ejemplo = archivo.read()
archivo.close()
arbol = analizar(texto_ejemplo)

reporte_estadisticas = GeneradorEstadisticas(
    arbol,
    "ejemplo_valido.md",
).generar()
assert "<td>Total de palabras</td><td>67</td>" in reporte_estadisticas
assert "<td>Total de párrafos</td><td>2</td>" in reporte_estadisticas
assert "<td>H1</td><td>1</td>" in reporte_estadisticas
assert "<td>H2</td><td>1</td>" in reporte_estadisticas
assert "<td>Listas de primer nivel</td><td>1</td>" in reporte_estadisticas
assert "<td>Profundidad máxima de listas</td><td>3</td>" in reporte_estadisticas
assert "<td>Cantidad de citas</td><td>1</td>" in reporte_estadisticas
assert "<td>Profundidad máxima de citas</td><td>2</td>" in reporte_estadisticas
assert "<td>Bloques de código</td><td>1</td>" in reporte_estadisticas
assert "<td>Tramos de negrita</td><td>1</td>" in reporte_estadisticas
assert "<td>Tramos de cursiva</td><td>1</td>" in reporte_estadisticas
assert "<td>Tramos de código en línea</td><td>1</td>" in reporte_estadisticas

reporte_indice = GeneradorIndice(arbol, "ejemplo_valido.md").generar()
assert 'href="reporte1_documento.html#seccion-1"' in reporte_indice
assert 'href="reporte1_documento.html#seccion-2"' in reporte_indice
reporte_html = GeneradorHTML(arbol, "ejemplo_valido.md").generar()
assert 'id="seccion-1"' in reporte_html
assert 'id="seccion-2"' in reporte_html

arbol_sin_encabezados = analizar("Un párrafo sin encabezado.\n")
reporte_vacio = GeneradorIndice(
    arbol_sin_encabezados,
    "sin_encabezados.md",
).generar()
assert "El documento no tiene encabezados" in reporte_vacio

dot = generar_dot(arbol)
assert dot.startswith("digraph ArbolDerivacion")
assert "#D0E1FD" in dot
assert "#D1F2D9" in dot
cantidad_nodos = dot.count(" [label=")
cantidad_aristas = dot.count(" -> ")
assert cantidad_aristas == cantidad_nodos - 1

print("Pruebas de reportes correctas.")
