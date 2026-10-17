from src.analizador_lexico import AnalizadorLexico
from src.analizador_sintactico import AnalizadorSintactico
from src.generador_html import GeneradorHTML
from src.gestor_errores import GestorErrores


def generar_html(texto, nombre_archivo):
    gestor_errores = GestorErrores()
    analizador_lexico = AnalizadorLexico(texto, gestor_errores)
    tokens = analizador_lexico.tokenizar()
    analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
    arbol = analizador_sintactico.parsear_documento()
    assert gestor_errores.cantidad() == 0
    generador = GeneradorHTML(arbol, nombre_archivo)
    return generador.generar()


archivo = open("ejemplos/ejemplo_valido.md", "r", encoding="utf-8")
texto_ejemplo = archivo.read()
archivo.close()
html_ejemplo = generar_html(texto_ejemplo, "ejemplo_valido.md")
assert "<h1" in html_ejemplo
assert "<strong>" in html_ejemplo
assert "<em>" in html_ejemplo
assert "<code>" in html_ejemplo
assert "<blockquote>" in html_ejemplo
assert "<hr>" in html_ejemplo
assert '<pre><code class="language-python">' in html_ejemplo
assert "<p>Este curso combina <strong>" in html_ejemplo
assert "<p>Fin del documento.</p>" in html_ejemplo

texto_lista = (
    "- Nivel 1\n"
    "  - Nivel 2\n"
    "    - Nivel 3\n"
)
html_lista = generar_html(texto_lista, "lista.md")
assert html_lista.count("<ul>") == 3

texto_cita = "> Nivel 1\n>> Nivel 2\n"
html_cita = generar_html(texto_cita, "cita.md")
primera_cierre = html_cita.index("</blockquote>")
assert html_cita[:primera_cierre].count("<blockquote>") == 2

html_escape = generar_html("Texto < & >\n```text\n< & >\n```\n", "escape.md")
assert "&lt; &amp; &gt;" in html_escape

print("Pruebas HTML correctas.")
