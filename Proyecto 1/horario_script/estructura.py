def _extraer_bloque_elemento(tokens, tipo_elemento):
    elementos = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.tipo == tipo_elemento:
            datos = {"identificador": None, "codigo": None, "linea": token.linea}
            j = i + 1
            atributo_actual = None
            identificador_asignado = False
            while j < len(tokens) and tokens[j].lexema != "]":
                actual = tokens[j]
                if actual.tipo == "PALABRA_RESERVADA":
                    atributo_actual = actual.lexema
                elif actual.tipo in ("CADENA", "ENTERO", "CATEGORIA", "DIA"):
                    valor = actual.lexema.strip('"') if actual.tipo == "CADENA" else actual.lexema
                    if atributo_actual is not None:
                        datos[atributo_actual] = valor
                        atributo_actual = None
                    elif not identificador_asignado:
                        datos["identificador"] = valor
                        identificador_asignado = True
                j += 1
            if datos.get("codigo") is None:
                datos["codigo"] = datos["identificador"]
            elementos.append(datos)
            i = j
        i += 1
    return elementos
def extraer_cursos(tokens):
    cursos = _extraer_bloque_elemento(tokens, "ELEMENTO_CURSO")
    for curso in cursos:
        curso["nombre"] = curso["identificador"]
    return cursos
def extraer_catedraticos(tokens):
    catedraticos = _extraer_bloque_elemento(tokens, "ELEMENTO_CATEDRATICO")
    for catedratico in catedraticos:
        catedratico["nombre"] = catedratico["identificador"]
    return catedraticos
def extraer_aulas(tokens):
    return _extraer_bloque_elemento(tokens, "ELEMENTO_AULA")