TRANSICIONES_AFD = [
    ("INICIO", "LEYENDO_LETRA", "letra"),
    ("LEYENDO_LETRA", "LEYENDO_LETRA", "letra"),
    ("LEYENDO_LETRA", "LEYENDO_GUION", "-"),
    ("LEYENDO_LETRA", "ACEPTA_PALABRA_RESERVADA", "fin de palabra (reservada)"),
    ("LEYENDO_LETRA", "ERROR_LEXICO", "fin de palabra (no reservada, sin guion)"),
    ("LEYENDO_GUION", "LEYENDO_DIGITOS_CODIGO", "digito"),
    ("LEYENDO_GUION", "ERROR_LEXICO", "no-digito (codigo mal formado)"),
    ("LEYENDO_DIGITOS_CODIGO", "LEYENDO_DIGITOS_CODIGO", "digito"),
    ("LEYENDO_DIGITOS_CODIGO", "ACEPTA_CODIGO", "separador"),
    ("LEYENDO_DIGITOS_CODIGO", "ERROR_LEXICO", "no-separador (codigo mal formado)"),

    ("INICIO", "LEYENDO_DIGITO", "digito"),
    ("LEYENDO_DIGITO", "LEYENDO_DIGITO", "digito"),
    ("LEYENDO_DIGITO", "LEYENDO_DOS_PUNTOS", ": (tras 2 digitos)"),
    ("LEYENDO_DIGITO", "ACEPTA_ENTERO", "separador"),
    ("LEYENDO_DOS_PUNTOS", "LEYENDO_MINUTOS", "digito"),
    ("LEYENDO_MINUTOS", "LEYENDO_MINUTOS", "digito"),
    ("LEYENDO_MINUTOS", "ACEPTA_HORA", "separador (2 digitos de minuto)"),
    ("LEYENDO_MINUTOS", "ERROR_LEXICO", "separador (minutos != 2 digitos, o rango invalido)"),

    ("INICIO", "LEYENDO_CADENA", "\""),
    ("LEYENDO_CADENA", "LEYENDO_CADENA", "cualquier caracter != \\n"),
    ("LEYENDO_CADENA", "ACEPTA_CADENA", "\""),
    ("LEYENDO_CADENA", "ERROR_LEXICO", "\\n o EOF (cadena sin cerrar)"),

    ("INICIO", "LEYENDO_COMENTARIO", "#"),
    ("LEYENDO_COMENTARIO", "ERROR_LEXICO", "caracter != # (tras primer #)"),
    ("LEYENDO_COMENTARIO", "LEYENDO_COMENTARIO", "cualquier caracter != \\n (tras ##)"),
    ("LEYENDO_COMENTARIO", "ACEPTA_COMENTARIO", "\\n o EOF"),

    ("INICIO", "ACEPTA_SIMBOLO", "{ } [ ] : ; ,"),
    ("INICIO", "ERROR_LEXICO", "caracter no reconocido"),
]

ESTADOS_ACEPTACION = {
    "ACEPTA_CODIGO", "ACEPTA_PALABRA_RESERVADA", "ACEPTA_HORA",
    "ACEPTA_ENTERO", "ACEPTA_CADENA", "ACEPTA_COMENTARIO", "ACEPTA_SIMBOLO",
}

ESTADO_INICIAL = "INICIO"
ESTADO_ERROR = "ERROR_LEXICO"


def generar_dot():
    lineas = ["digraph AFD_HorarioScript {", "    rankdir=LR;", "    fontname=\"Arial\";"]
    lineas.append('    node [shape=circle, fontname="Arial", fontsize=10];')

    lineas.append(f'    {ESTADO_INICIAL} [shape=doublecircle, style=filled, fillcolor="#dceefb"];')
    for estado in ESTADOS_ACEPTACION:
        lineas.append(f'    {estado} [shape=doublecircle, style=filled, fillcolor="#e2f7e1"];')
    lineas.append(f'    {ESTADO_ERROR} [shape=box, style=filled, fillcolor="#fbdada"];')

    for origen, destino, etiqueta in TRANSICIONES_AFD:
        etiqueta_escapada = etiqueta.replace('"', '\\"')
        lineas.append(f'    {origen} -> {destino} [label="{etiqueta_escapada}"];')

    lineas.append("}")
    return "\n".join(lineas)


def exportar_dot(ruta_salida):
    from pathlib import Path
    contenido = generar_dot()
    Path(ruta_salida).write_text(contenido, encoding="utf-8")
    return contenido