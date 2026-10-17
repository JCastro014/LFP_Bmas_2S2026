def generar_dot(arbol):
    lineas = []
    lineas.append("digraph ArbolDerivacion {")
    lineas.append("    rankdir=TB;")
    lineas.append(
        '    node [shape=box, style=filled, fontname="Arial"];'
    )
    contador = [0]
    _agregar_nodo(arbol, None, contador, lineas)
    lineas.append("}")
    return "\n".join(lineas)


def exportar_dot(arbol, ruta):
    contenido = generar_dot(arbol)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    return contenido


def _agregar_nodo(nodo, padre, contador, lineas):
    identificador = "n" + str(contador[0])
    contador[0] += 1

    if nodo.tipo == nodo.tipo.upper():
        etiqueta = _etiqueta_hoja(nodo)
        linea = (
            '    '
            + identificador
            + ' [label="'
            + etiqueta
            + '", shape=box, style="rounded,filled", fillcolor="#D1F2D9"];'
        )
    else:
        etiqueta = "<" + _escapar_dot(nodo.tipo) + ">"
        color = "#D0E1FD"
        fontcolor = ""
        if padre is None:
            color = "#2E75B6"
            fontcolor = ', fontcolor="white"'
        linea = (
            '    '
            + identificador
            + ' [label="'
            + etiqueta
            + '", shape=ellipse, style=filled, fillcolor="'
            + color
            + '"'
            + fontcolor
            + "];"
        )
    lineas.append(linea)

    if padre is not None:
        lineas.append("    " + padre + " -> " + identificador + ";")

    for hijo in nodo.hijos:
        _agregar_nodo(hijo, identificador, contador, lineas)


def _etiqueta_hoja(nodo):
    lexema = nodo.lexema
    simplificado = ""
    cantidad = 0
    largo = len(lexema)

    for caracter in lexema:
        if caracter == "\n" or caracter == "\r":
            caracter = " "
        if cantidad < 20:
            simplificado += caracter
        cantidad += 1

    if largo > 20:
        simplificado += "..."

    etiqueta = _escapar_dot(nodo.tipo)
    if simplificado != "":
        etiqueta += "\\n" + _escapar_dot(simplificado)
    return etiqueta


def _escapar_dot(texto):
    resultado = ""
    for caracter in texto:
        if caracter == "\\":
            resultado += "\\\\"
        elif caracter == '"':
            resultado += '\\"'
        else:
            resultado += caracter
    return resultado
