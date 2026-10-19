import os

from src.analizador_lexico import AnalizadorLexico
from src.analizador_sintactico import AnalizadorSintactico
from src.gestor_errores import GestorErrores


casos = [
    [
        1,
        "ejemplo_valido.md",
        "Documento válido con listas y citas anidadas.",
        0,
        [],
        3,
        2,
        "",
    ],
    [
        2,
        "lista_3_niveles.md",
        "Lista con tres niveles de indentación.",
        0,
        [],
        3,
        0,
        "",
    ],
    [
        3,
        "citas_anidadas.md",
        "Dos líneas de cita con dos niveles.",
        0,
        [],
        0,
        2,
        "",
    ],
    [
        4,
        "negrita_sin_cerrar.md",
        "Marcador de negrita sin cierre.",
        1,
        [["NEGRITA_SIN_CERRAR", "Léxico", 1, 9]],
        0,
        0,
        "",
    ],
    [
        5,
        "cursiva_sin_cerrar.md",
        "Marcador de cursiva sin cierre.",
        1,
        [["CURSIVA_SIN_CERRAR", "Léxico", 1, 9]],
        0,
        0,
        "",
    ],
    [
        6,
        "codigo_inline_sin_cerrar.md",
        "Código en línea sin cierre.",
        1,
        [["CODIGO_INLINE_SIN_CERRAR", "Léxico", 1, 9]],
        0,
        0,
        "",
    ],
    [
        7,
        "encabezado_invalido.md",
        "Encabezado con más de seis numerales.",
        1,
        [["ENCABEZADO_INVALIDO", "Léxico", 1, 1]],
        0,
        0,
        "",
    ],
    [
        8,
        "bloque_sin_cerrar.md",
        "Bloque de código sin cierre.",
        1,
        [["BLOQUE_CODIGO_SIN_CERRAR", "Léxico", 1, 1]],
        0,
        0,
        "",
    ],
    [
        9,
        "indentacion_invalida.md",
        "Lista que salta dos niveles de indentación.",
        1,
        [["INDENTACION_INVALIDA", "Sintáctico", 2, 1]],
        0,
        0,
        "",
    ],
    [
        10,
        "cita_mal_formada.md",
        "Marcador de cita sin espacio después.",
        1,
        [["CITA_MAL_FORMADA", "Sintáctico", 1, 1]],
        0,
        0,
        "",
    ],
    [
        11,
        "borde_vacio.md",
        "Archivo vacío.",
        0,
        [],
        0,
        0,
        "",
    ],
    [
        12,
        "borde_sin_espacio.md",
        "Numeral sin espacio: debe quedar como texto.",
        0,
        [],
        0,
        0,
        "TEXTO",
    ],
    [
        13,
        "borde_negrita_cursiva.md",
        "Cursiva anidada dentro de negrita.",
        0,
        [],
        0,
        0,
        "",
    ],
]


def escapar_html(texto):
    resultado = ""
    for caracter in texto:
        if caracter == "&":
            resultado += "&amp;"
        elif caracter == "<":
            resultado += "&lt;"
        elif caracter == ">":
            resultado += "&gt;"
        else:
            resultado += caracter
    return resultado


def describir_esperado(caso):
    numero_errores = caso[3]
    errores_esperados = caso[4]
    profundidad_listas = caso[5]
    profundidad_citas = caso[6]
    primer_tipo = caso[7]

    if numero_errores == 0:
        texto = "0 errores"
        if caso[0] != 11:
            texto += ", profundidad de listas " + str(profundidad_listas)
            texto += ", profundidad de citas " + str(profundidad_citas)
        if primer_tipo != "":
            texto += ", primer token " + primer_tipo
        return texto

    error = errores_esperados[0]
    texto = (
        "1 error "
        + error[0]
        + ", "
        + error[1]
        + ", línea "
        + str(error[2])
        + ", columna "
        + str(error[3])
    )
    return texto


def analizar_caso(caso):
    ruta = os.path.join("ejemplos", caso[1])
    with open(ruta, "r", encoding="utf-8") as archivo:
        entrada = archivo.read()

    gestor_errores = GestorErrores()
    analizador_lexico = AnalizadorLexico(entrada, gestor_errores)
    tokens = analizador_lexico.tokenizar()
    analizador_sintactico = AnalizadorSintactico(tokens, gestor_errores)
    arbol = analizador_sintactico.parsear_documento()

    errores_obtenidos = []
    for error in gestor_errores.errores:
        errores_obtenidos.append(
            [error.tipo, error.fase, error.linea, error.columna]
        )

    obtenido = {
        "entrada": entrada,
        "errores": errores_obtenidos,
        "cantidad": gestor_errores.cantidad(),
        "listas": None,
        "citas": None,
        "primer_tipo": "",
    }

    if gestor_errores.cantidad() == 0:
        obtenido["listas"] = arbol.profundidad_maxima_listas()
        obtenido["citas"] = arbol.profundidad_maxima_citas()
    if len(tokens) > 0:
        obtenido["primer_tipo"] = tokens[0].tipo

    cumple = obtenido["cantidad"] == caso[3]
    if cumple and obtenido["errores"] != caso[4]:
        cumple = False
    if cumple and caso[3] == 0 and caso[0] != 11:
        if obtenido["listas"] != caso[5]:
            cumple = False
        if obtenido["citas"] != caso[6]:
            cumple = False
    if cumple and caso[7] != "":
        if obtenido["primer_tipo"] != caso[7]:
            cumple = False

    obtenido["cumple"] = cumple
    return obtenido


def describir_obtenido(obtenido):
    errores = obtenido["errores"]
    if obtenido["cantidad"] == 0:
        texto = "0 errores"
        if obtenido["listas"] is not None:
            texto += ", profundidad de listas " + str(obtenido["listas"])
            texto += ", profundidad de citas " + str(obtenido["citas"])
        if obtenido["primer_tipo"] != "":
            texto += ", primer token " + obtenido["primer_tipo"]
        return texto

    texto = str(obtenido["cantidad"]) + " error(es): "
    numero = 0
    for error in errores:
        if numero > 0:
            texto += "; "
        texto += (
            error[0]
            + ", "
            + error[1]
            + ", línea "
            + str(error[2])
            + ", columna "
            + str(error[3])
        )
        numero += 1
    return texto


def generar_html(resultados, cantidad_cumplen):
    html = "<!DOCTYPE html>\n"
    html += '<html lang="es">\n'
    html += "<head>\n"
    html += '<meta charset="utf-8">\n'
    html += "<title>Casos de prueba</title>\n"
    html += "<style>\n"
    html += "body {\n"
    html += "    font-family: Verdana, sans-serif;\n"
    html += "    background: #f4f1ea;\n"
    html += "    color: #222;\n"
    html += "    margin: 24px;\n"
    html += "}\n"
    html += "table {\n"
    html += "    width: 100%;\n"
    html += "    border-collapse: collapse;\n"
    html += "    margin-bottom: 10px;\n"
    html += "}\n"
    html += "th, td {\n"
    html += "    border: 1px solid #8b3a3a;\n"
    html += "    padding: 8px;\n"
    html += "    text-align: left;\n"
    html += "    vertical-align: top;\n"
    html += "}\n"
    html += "pre {\n"
    html += "    white-space: pre-wrap;\n"
    html += "    margin: 0;\n"
    html += "}\n"
    html += ".captura {\n"
    html += "    height: 90px;\n"
    html += "    border: 1px solid #999;\n"
    html += "    margin-bottom: 24px;\n"
    html += "    padding: 8px;\n"
    html += "}\n"
    html += "</style>\n"
    html += "</head>\n"
    html += "<body>\n"
    html += "<h1>Casos de prueba</h1>\n"

    for registro in resultados:
        caso = registro[0]
        obtenido = registro[1]
        resultado = "Cumple"
        if not obtenido["cumple"]:
            resultado = "No cumple"

        html += "<h2>Caso " + str(caso[0]) + "</h2>\n"
        html += "<table>\n"
        html += "<tr><th>Número</th><td>" + str(caso[0]) + "</td></tr>\n"
        html += "<tr><th>Archivo</th><td>" + caso[1] + "</td></tr>\n"
        html += (
            "<tr><th>Descripción</th><td>"
            + escapar_html(caso[2])
            + "</td></tr>\n"
        )
        html += (
            "<tr><th>Entrada</th><td><pre>"
            + escapar_html(obtenido["entrada"])
            + "</pre></td></tr>\n"
        )
        html += (
            "<tr><th>Esperado</th><td>"
            + escapar_html(describir_esperado(caso))
            + "</td></tr>\n"
        )
        html += (
            "<tr><th>Obtenido</th><td>"
            + escapar_html(describir_obtenido(obtenido))
            + "</td></tr>\n"
        )
        html += "<tr><th>Resultado</th><td>" + resultado + "</td></tr>\n"
        html += "</table>\n"
        html += '<div class="captura">Captura de la GUI:</div>\n'

    html += (
        "<h2>"
        + str(cantidad_cumplen)
        + " de "
        + str(len(casos))
        + " casos cumplen</h2>\n"
    )
    html += "</body>\n</html>\n"
    return html


def main():
    resultados = []
    cantidad_cumplen = 0

    for caso in casos:
        obtenido = analizar_caso(caso)
        resultados.append([caso, obtenido])
        if obtenido["cumple"]:
            cantidad_cumplen += 1
            estado = "Cumple"
        else:
            estado = "No cumple"
        print(
            str(caso[0])
            + ". "
            + caso[1]
            + ": "
            + estado
            + " — "
            + describir_obtenido(obtenido)
        )

    os.makedirs("docs", exist_ok=True)
    with open("docs/casos_de_prueba.html", "w", encoding="utf-8") as archivo:
        archivo.write(generar_html(resultados, cantidad_cumplen))

    print(
        str(cantidad_cumplen)
        + " de "
        + str(len(casos))
        + " casos cumplen."
    )


if __name__ == "__main__":
    main()
