from .error_lexico import ErrorLexico
from .gestor_errores import GestorErrores
from .token import Token


class AnalizadorLexico:
    BLOQUES = {
        "HORARIO": "BLOQUE_HORARIO",
        "CURSOS": "BLOQUE_CURSOS",
        "CATEDRATICOS": "BLOQUE_CATEDRATICOS",
        "AULAS": "BLOQUE_AULAS",
        "CLASES": "BLOQUE_CLASES",
    }

    ELEMENTOS = {
        "curso": "ELEMENTO_CURSO",
        "catedratico": "ELEMENTO_CATEDRATICO",
        "aula": "ELEMENTO_AULA",
        "clase": "ELEMENTO_CLASE",
    }

    ATRIBUTOS = {
        "codigo",
        "creditos",
        "categoria",
        "capacidad",
        "edificio",
        "dia",
        "inicio",
        "fin",
        "seccion",
    }

    RELACIONES = {
        "con": "RELACION_CON",
        "en": "RELACION_EN",
    }

    DIAS = {
        "LUNES",
        "MARTES",
        "MIERCOLES",
        "JUEVES",
        "VIERNES",
        "SABADO",
    }

    CATEGORIAS = {
        "TITULAR",
        "INTERINO",
        "AUXILIAR",
    }

    SIMBOLOS = "{}[]:;,"

    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.numero_token = 1
        self.gestor_errores = GestorErrores()
        self.esperando_dia = False

    @property
    def errores(self):
        return self.gestor_errores.errores

    def analizar(self):
        tokens = []
        while True:
            token = self.siguiente_token()
            if token is None:
                return tokens
            tokens.append(token)

    def siguiente_token(self):
        self._ignorar_espacios()

        if self._termino():
            return None

        linea_inicial = self.linea
        columna_inicial = self.columna
        caracter = self._actual()

        if self._es_letra(caracter):
            return self._leer_palabra_o_codigo(linea_inicial, columna_inicial)
        if self._es_digito(caracter):
            return self._leer_numero_o_hora(linea_inicial, columna_inicial)
        if caracter == '"':
            return self._leer_cadena(linea_inicial, columna_inicial)
        if caracter == '#':
            return self._leer_comentario(linea_inicial, columna_inicial)
        if caracter in self.SIMBOLOS:
            self._avanzar()
            return self._crear_token(caracter, "SIMBOLO", linea_inicial, columna_inicial)

        self._registrar_error(
            caracter,
            "CARACTER_NO_RECONOCIDO",
            f"Carácter no reconocido: '{caracter}' en línea {linea_inicial}, columna {columna_inicial}",
            linea_inicial,
            columna_inicial,
        )
        self._avanzar()
        return self.siguiente_token()

    def _leer_palabra_o_codigo(self, linea, columna):
        inicio = self.posicion
        while not self._termino() and self._es_letra(self._actual()):
            self._avanzar()

        cantidad_letras = self.posicion - inicio
        if not self._termino() and self._actual() == '-':
            self._avanzar()
            digitos_inicio = self.posicion
            while not self._termino() and self._es_digito(self._actual()):
                self._avanzar()

            if self.posicion == digitos_inicio:
                lexema = self._obtener_lexema(inicio)
                self._registrar_error(
                    lexema,
                    "CODIGO_MAL_FORMADO",
                    f"Código mal formado: '{lexema}' en línea {linea}, columna {columna}",
                    linea,
                    columna,
                )
                self._recuperar()
                return self.siguiente_token()

            if not self._termino() and not self._es_separador(self._actual()):
                while not self._termino() and not self._es_separador(self._actual()):
                    self._avanzar()
                lexema = self._obtener_lexema(inicio)
                self._registrar_error(
                    lexema,
                    "CODIGO_MAL_FORMADO",
                    f"Código mal formado: '{lexema}' en línea {linea}, columna {columna}",
                    linea,
                    columna,
                )
                return self.siguiente_token()

            lexema = self._obtener_lexema(inicio)
            return self._crear_token(lexema, "CODIGO", linea, columna)

        if not self._termino() and self._es_digito(self._actual()):
            while not self._termino() and not self._es_separador(self._actual()):
                self._avanzar()
            lexema = self._obtener_lexema(inicio)
            self._registrar_error(
                lexema,
                "CODIGO_MAL_FORMADO",
                f"Código mal formado: '{lexema}' en línea {linea}, columna {columna}",
                linea,
                columna,
            )
            return self.siguiente_token()

        lexema = self._obtener_lexema(inicio)
        tipo = self._tipo_de_palabra(lexema, cantidad_letras)
        if tipo is None:
            if self.esperando_dia:
                self._registrar_error(
                    lexema,
                    "DIA_NO_RECONOCIDO",
                    f"Día no reconocido: '{lexema}' en línea {linea}, columna {columna}",
                    linea,
                    columna,
                )
                self.esperando_dia = False
            else:
                self._registrar_error(
                    lexema,
                    "CODIGO_MAL_FORMADO",
                    f"Código mal formado: '{lexema}' en línea {linea}, columna {columna}",
                    linea,
                    columna,
                )
            return self.siguiente_token()
        if tipo == "DIA":
            self.esperando_dia = False
        elif tipo == "PALABRA_RESERVADA" and lexema == "dia":
            self.esperando_dia = True
        return self._crear_token(lexema, tipo, linea, columna)

    def _leer_numero_o_hora(self, linea, columna):
        inicio = self.posicion
        while not self._termino() and self._es_digito(self._actual()):
            self._avanzar()

        cantidad = self.posicion - inicio
        if cantidad == 2 and not self._termino() and self._actual() == ':':
            self._avanzar()
            minutos_inicio = self.posicion
            while not self._termino() and self._es_digito(self._actual()):
                self._avanzar()

            minutos = self.posicion - minutos_inicio
            if minutos != 2:
                lexema = self._obtener_lexema(inicio)
                self._registrar_error(
                    lexema,
                    "HORA_FUERA_DE_RANGO",
                    f"Hora fuera de rango en línea {linea}, columna {columna}: debe tener formato HH:MM",
                    linea,
                    columna,
                )
                self._recuperar()
                return self.siguiente_token()

            lexema = self._obtener_lexema(inicio)
            if not self._hora_valida(lexema):
                self._registrar_error(
                    lexema,
                    "HORA_FUERA_DE_RANGO",
                    f"Hora fuera de rango: '{lexema}' en línea {linea}, columna {columna}",
                    linea,
                    columna,
                )
            return self._crear_token(lexema, "HORA", linea, columna)

        if not self._termino() and not self._es_separador(self._actual()):
            while not self._termino() and not self._es_separador(self._actual()):
                self._avanzar()
            lexema = self._obtener_lexema(inicio)
            self._registrar_error(
                lexema,
                "HORA_FUERA_DE_RANGO",
                f"Hora fuera de rango: '{lexema}' en línea {linea}, columna {columna}",
                linea,
                columna,
            )
            return self.siguiente_token()

        lexema = self._obtener_lexema(inicio)
        if self.esperando_dia:
            self._registrar_error(
                lexema,
                "DIA_NO_RECONOCIDO",
                f"Día no reconocido: '{lexema}' en línea {linea}, columna {columna}",
                linea,
                columna,
            )
            self.esperando_dia = False
        return self._crear_token(lexema, "ENTERO", linea, columna)

    def _leer_cadena(self, linea, columna):
        inicio = self.posicion
        self._avanzar()
        cerrada = False

        while not self._termino() and self._actual() != '\n':
            if self._actual() == '"':
                self._avanzar()
                cerrada = True
                break
            self._avanzar()

        lexema = self._obtener_lexema(inicio)
        if not cerrada:
            self._registrar_error(
                lexema,
                "CADENA_SIN_CERRAR",
                f"Cadena sin cerrar iniciada en línea {linea}, columna {columna}",
                linea,
                columna,
            )
            return self.siguiente_token()
        return self._crear_token(lexema, "CADENA", linea, columna)

    def _leer_comentario(self, linea, columna):
        inicio = self.posicion
        self._avanzar()
        if self._termino() or self._actual() != '#':
            self._registrar_error(
                '#',
                "CARACTER_NO_RECONOCIDO",
                f"Carácter no reconocido: '#' en línea {linea}, columna {columna}",
                linea,
                columna,
            )
            return self.siguiente_token()

        self._avanzar()
        while not self._termino() and self._actual() != '\n':
            self._avanzar()
        lexema = self._obtener_lexema(inicio)
        return self._crear_token(lexema, "COMENTARIO_LINEA", linea, columna)

    def _tipo_de_palabra(self, lexema, cantidad_letras):
        if lexema in self.BLOQUES:
            return self.BLOQUES[lexema]
        if lexema in self.ELEMENTOS:
            return self.ELEMENTOS[lexema]
        if lexema in self.ATRIBUTOS:
            return "PALABRA_RESERVADA"
        if lexema in self.RELACIONES:
            return self.RELACIONES[lexema]
        if lexema in self.DIAS:
            return "DIA"
        if lexema in self.CATEGORIAS:
            return "CATEGORIA"
        if cantidad_letras > 0:
            return None
        return None

    def _hora_valida(self, lexema):
        hora = int(lexema[0] + lexema[1])
        minuto = int(lexema[3] + lexema[4])
        if minuto > 59:
            return False
        return 6 <= hora <= 21

    def _recuperar(self):
        while not self._termino() and not self._es_separador(self._actual()):
            self._avanzar()

    def _ignorar_espacios(self):
        while not self._termino() and self._actual() in ' \t\r\n':
            self._avanzar()

    def _crear_token(self, lexema, tipo, linea, columna):
        token = Token(self.numero_token, lexema, tipo, linea, columna)
        self.numero_token += 1
        return token

    def _registrar_error(self, lexema, tipo, descripcion, linea, columna):
        self.gestor_errores.agregar(
            lexema,
            tipo,
            descripcion,
            linea,
            columna,
        )

    def _obtener_lexema(self, inicio):
        lexema = ""
        posicion = inicio
        while posicion < self.posicion:
            lexema += self.texto[posicion]
            posicion += 1
        return lexema

    def _actual(self):
        return self.texto[self.posicion]

    def _avanzar(self):
        caracter = self.texto[self.posicion]
        self.posicion += 1
        if caracter == '\n':
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1

    def _termino(self):
        return self.posicion >= len(self.texto)

    def _es_letra(self, caracter):
        return (
            ('a' <= caracter <= 'z')
            or ('A' <= caracter <= 'Z')
            or caracter == '_'
        )

    def _es_digito(self, caracter):
        return '0' <= caracter <= '9'

    def _es_separador(self, caracter):
        return caracter in ' \t\r\n{}[]:;,"'
