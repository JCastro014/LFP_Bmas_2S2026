
def _minutos(hora_texto):

    horas = int(hora_texto[0:2])
    minutos = int(hora_texto[3:5])
    return horas * 60 + minutos


def extraer_clases(tokens):
    clases = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.tipo == "ELEMENTO_CLASE":
            clase = {
                "curso": None,
                "catedratico": None,
                "aula": None,
                "dia": None,
                "inicio": None,
                "fin": None,
                "seccion": None,
                "linea": token.linea,
            }
            j = i + 1
            relacion_esperada = None
            while j < len(tokens) and tokens[j].lexema != "]":
                actual = tokens[j]
                if actual.tipo == "CADENA":
                    if clase["curso"] is None:
                        clase["curso"] = actual.lexema.strip('"')
                    elif relacion_esperada == "con":
                        clase["catedratico"] = actual.lexema.strip('"')
                        relacion_esperada = None
                    elif relacion_esperada == "en":
                        clase["aula"] = actual.lexema.strip('"')
                        relacion_esperada = None
                    elif clase["seccion"] is None and clase["dia"] is not None:
                        clase["seccion"] = actual.lexema.strip('"')

                elif actual.tipo == "RELACION_CON":
                    relacion_esperada = "con"
                elif actual.tipo == "RELACION_EN":
                    relacion_esperada = "en"

                elif actual.tipo == "DIA":
                    clase["dia"] = actual.lexema
                elif actual.tipo == "HORA":
                    if clase["inicio"] is None:
                        clase["inicio"] = actual.lexema
                    else:
                        clase["fin"] = actual.lexema

                j += 1

            clases.append(clase)
            i = j

        i += 1

    return clases


def detectar_choques(clases):
    choques = []

    for a in range(len(clases)):
        for b in range(a + 1, len(clases)):
            clase1 = clases[a]
            clase2 = clases[b]

            if clase1["dia"] != clase2["dia"]:
                continue

            inicio1 = _minutos(clase1["inicio"])
            fin1 = _minutos(clase1["fin"])
            inicio2 = _minutos(clase2["inicio"])
            fin2 = _minutos(clase2["fin"])

            se_traslapan = inicio1 < fin2 and inicio2 < fin1
            if not se_traslapan:
                continue

            mismo_catedratico = clase1["catedratico"] == clase2["catedratico"]
            mismo_aula = clase1["aula"] == clase2["aula"]

            if mismo_catedratico or mismo_aula:
                choques.append({
                    "clase1": clase1,
                    "clase2": clase2,
                    "motivo": "catedratico" if mismo_catedratico else "aula",
                })

    return choques
