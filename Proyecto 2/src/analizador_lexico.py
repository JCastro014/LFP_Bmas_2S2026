from .token import Token


class AnalizadorLexico:
    def __init__(self, texto, gestor_errores):
        self.texto = texto
        self.gestor_errores = gestor_errores
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.numero_token = 1
        self.pendientes = []
        self.token_eof = None

    def siguiente_token(self):
        if len(self.pendientes) == 0:
            if self._termino():
                if self.token_eof is None:
                    self.token_eof = self._crear_token(
                        "",
                        "EOF",
                        self.linea,
                        self.columna,
                    )
                return self.token_eof
            self._leer_linea()

        return self.pendientes.pop(0)

    def tokenizar(self):
        tokens = []
        token = self.siguiente_token()
        while token.tipo != "EOF":
            tokens.append(token)
            token = self.siguiente_token()
        tokens.append(token)
        return tokens

    def _leer_linea(self):
        posicion_inicio = self.posicion
        linea_inicio = self.linea
        columna_inicio = self.columna

        espacios_iniciales = 0
        while self._ver(espacios_iniciales) == " ":
            espacios_iniciales += 1

        posicion_contenido = posicion_inicio + espacios_iniciales
        caracter = self._caracter_en(posicion_contenido)

        if caracter == "" or caracter == "\n" or caracter == "\r":
            self._consumir_espacios(espacios_iniciales)
            self._consumir_fin_linea()
            self.pendientes.append(
                self._crear_token(
                    "",
                    "SALTO_PARRAFO",
                    linea_inicio,
                    columna_inicio,
                )
            )
            return

        if espacios_iniciales == 0 and self._es_regla_horizontal():
            self._leer_regla_horizontal()
            return

        if espacios_iniciales == 0 and caracter == "#":
            cantidad_numerales = self._cantidad_caracteres("#", 0)
            if cantidad_numerales > 6:
                self._registrar_error(
                    "#" * cantidad_numerales,
                    "ENCABEZADO_INVALIDO",
                    "Encabezado inválido en línea "
                    + str(linea_inicio)
                    + ": máximo 6 niveles",
                    linea_inicio,
                    columna_inicio,
                )
                self._leer_toda_linea_como_texto()
                return
            if (
                cantidad_numerales >= 1
                and cantidad_numerales <= 6
                and self._ver(cantidad_numerales) == " "
            ):
                self._leer_encabezado(cantidad_numerales)
                return

        if (
            caracter in "-*+"
            and self._caracter_en(posicion_contenido + 1) == " "
        ):
            self._leer_vineta(espacios_iniciales)
            return

        self._leer_texto()

    def _leer_regla_horizontal(self):
        linea = self.linea
        columna = self.columna
        inicio = self.posicion

        while not self._termino() and self._actual() == "-":
            self._avanzar()

        lexema = self._obtener_lexema(inicio)
        self.pendientes.append(
            self._crear_token(
                lexema,
                "REGLA_HORIZONTAL",
                linea,
                columna,
            )
        )
        self._saltar_espacios_finales()
        self._agregar_fin_linea()

    def _leer_encabezado(self, cantidad_numerales):
        linea = self.linea
        columna = self.columna
        inicio = self.posicion

        cantidad = 0
        while (
            not self._termino()
            and self._actual() == "#"
            and cantidad < cantidad_numerales
        ):
            self._avanzar()
            cantidad += 1

        lexema = self._obtener_lexema(inicio)
        self.pendientes.append(
            self._crear_token(lexema, "NUMERAL", linea, columna)
        )
        self._avanzar()

        if not self._termino() and not self._es_fin_linea():
            self._leer_texto()
        else:
            self._agregar_fin_linea()

    def _leer_vineta(self, espacios_iniciales):
        self._consumir_espacios(espacios_iniciales)
        linea = self.linea
        columna = self.columna
        lexema = self._actual()
        self._avanzar()
        self.pendientes.append(
            self._crear_token(lexema, "VIÑETA", linea, columna)
        )
        self._avanzar()

        if not self._termino() and not self._es_fin_linea():
            self._leer_texto()
        else:
            self._agregar_fin_linea()

    def _leer_texto(self):
        negrita_abierta = False
        cursiva_abierta = False
        token_negrita = None
        token_cursiva = None
        linea_negrita = 0
        columna_negrita = 0
        linea_cursiva = 0
        columna_cursiva = 0
        inicio_texto = self.posicion
        linea_texto = self.linea
        columna_texto = self.columna

        while not self._termino() and not self._es_fin_linea():
            if self._actual() == "*" and self._ver(1) == "*":
                self._agregar_texto_pendiente(
                    inicio_texto,
                    linea_texto,
                    columna_texto,
                )
                linea = self.linea
                columna = self.columna
                inicio = self.posicion
                self._avanzar()
                self._avanzar()
                lexema = self._obtener_lexema(inicio)
                token = self._crear_token(lexema, "NEGRITA", linea, columna)
                self.pendientes.append(token)

                if negrita_abierta:
                    negrita_abierta = False
                    token_negrita = None
                else:
                    negrita_abierta = True
                    token_negrita = token
                    linea_negrita = linea
                    columna_negrita = columna

                inicio_texto = self.posicion
                linea_texto = self.linea
                columna_texto = self.columna
            elif self._actual() == "*":
                self._agregar_texto_pendiente(
                    inicio_texto,
                    linea_texto,
                    columna_texto,
                )
                linea = self.linea
                columna = self.columna
                inicio = self.posicion
                self._avanzar()
                lexema = self._obtener_lexema(inicio)
                token = self._crear_token(lexema, "CURSIVA", linea, columna)
                self.pendientes.append(token)

                if cursiva_abierta:
                    cursiva_abierta = False
                    token_cursiva = None
                else:
                    cursiva_abierta = True
                    token_cursiva = token
                    linea_cursiva = linea
                    columna_cursiva = columna

                inicio_texto = self.posicion
                linea_texto = self.linea
                columna_texto = self.columna
            elif (
                self._actual() == "`"
                and self._ver(1) == "`"
                and self._ver(2) == "`"
            ):
                self._avanzar()
                self._avanzar()
                self._avanzar()
            elif self._actual() == "`":
                posicion_cierre = self._buscar_cierre_codigo()
                if posicion_cierre == -1:
                    linea = self.linea
                    columna = self.columna
                    self._registrar_error(
                        "`",
                        "CODIGO_INLINE_SIN_CERRAR",
                        "Código en línea sin cerrar iniciado en línea "
                        + str(linea)
                        + ", columna "
                        + str(columna),
                        linea,
                        columna,
                    )
                    self._avanzar()
                else:
                    self._agregar_texto_pendiente(
                        inicio_texto,
                        linea_texto,
                        columna_texto,
                    )
                    self._leer_codigo_en_linea(posicion_cierre)
                    inicio_texto = self.posicion
                    linea_texto = self.linea
                    columna_texto = self.columna
            else:
                self._avanzar()

        self._agregar_texto_pendiente(
            inicio_texto,
            linea_texto,
            columna_texto,
        )

        if negrita_abierta:
            self._registrar_error(
                token_negrita.lexema,
                "NEGRITA_SIN_CERRAR",
                "Negrita sin cerrar iniciada en línea "
                + str(linea_negrita)
                + ", columna "
                + str(columna_negrita),
                linea_negrita,
                columna_negrita,
            )
            token_negrita.tipo = "TEXTO"

        if cursiva_abierta:
            self._registrar_error(
                token_cursiva.lexema,
                "CURSIVA_SIN_CERRAR",
                "Cursiva sin cerrar iniciada en línea "
                + str(linea_cursiva)
                + ", columna "
                + str(columna_cursiva),
                linea_cursiva,
                columna_cursiva,
            )
            token_cursiva.tipo = "TEXTO"

        self._agregar_fin_linea()

    def _agregar_texto_pendiente(self, inicio, linea, columna):
        if inicio < self.posicion:
            lexema = self._obtener_lexema(inicio)
            self.pendientes.append(
                self._crear_token(lexema, "TEXTO", linea, columna)
            )

    def _buscar_cierre_codigo(self):
        posicion = self.posicion + 1
        while posicion < len(self.texto):
            if self.texto[posicion] == "\n" or self.texto[posicion] == "\r":
                return -1
            if self.texto[posicion] == "`":
                return posicion
            posicion += 1
        return -1

    def _leer_codigo_en_linea(self, posicion_cierre):
        linea = self.linea
        columna = self.columna
        inicio = self.posicion
        self._avanzar()
        lexema = self._obtener_lexema(inicio)
        self.pendientes.append(
            self._crear_token(lexema, "CODIGO_INLINE", linea, columna)
        )

        linea_literal = self.linea
        columna_literal = self.columna
        inicio_literal = self.posicion
        while self.posicion < posicion_cierre:
            self._avanzar()
        lexema_literal = self._obtener_lexema(inicio_literal)
        self.pendientes.append(
            self._crear_token(
                lexema_literal,
                "TEXTO_LITERAL",
                linea_literal,
                columna_literal,
            )
        )

        linea_cierre = self.linea
        columna_cierre = self.columna
        inicio_cierre = self.posicion
        self._avanzar()
        lexema_cierre = self._obtener_lexema(inicio_cierre)
        self.pendientes.append(
            self._crear_token(
                lexema_cierre,
                "CODIGO_INLINE",
                linea_cierre,
                columna_cierre,
            )
        )

    def _leer_toda_linea_como_texto(self):
        self._leer_texto()

    def _consumir_espacios(self, cantidad):
        contador = 0
        while contador < cantidad and not self._termino():
            self._avanzar()
            contador += 1

    def _saltar_espacios_finales(self):
        while not self._termino() and self._actual() == " ":
            self._avanzar()

    def _agregar_fin_linea(self):
        linea = self.linea
        columna = self.columna
        self._consumir_fin_linea()
        self.pendientes.append(
            self._crear_token(
                "",
                "FIN_LINEA",
                linea,
                columna,
            )
        )

    def _consumir_fin_linea(self):
        while not self._termino() and self._actual() == "\r":
            self._avanzar()
        if not self._termino() and self._actual() == "\n":
            self._avanzar()

    def _es_regla_horizontal(self):
        cantidad_guiones = self._cantidad_caracteres("-", 0)
        if cantidad_guiones < 3:
            return False

        desplazamiento = cantidad_guiones
        while self._ver(desplazamiento) == " ":
            desplazamiento += 1

        return self._ver(desplazamiento) in ("", "\r", "\n")

    def _cantidad_caracteres(self, caracter, desplazamiento):
        cantidad = 0
        while self._ver(desplazamiento + cantidad) == caracter:
            cantidad += 1
        return cantidad

    def _caracter_en(self, posicion):
        if posicion >= len(self.texto):
            return ""
        return self.texto[posicion]

    def _actual(self):
        return self._caracter_en(self.posicion)

    def _avanzar(self):
        if self._termino():
            return

        caracter = self.texto[self.posicion]
        self.posicion += 1
        if caracter == "\n":
            self.linea += 1
            self.columna = 1
        elif caracter != "\r":
            self.columna += 1

    def _termino(self):
        return self.posicion >= len(self.texto)

    def _ver(self, cantidad):
        posicion = self.posicion + cantidad
        if posicion >= len(self.texto):
            return ""
        return self.texto[posicion]

    def _obtener_lexema(self, inicio):
        lexema = ""
        posicion = inicio
        while posicion < self.posicion:
            caracter = self.texto[posicion]
            if caracter != "\r":
                lexema = lexema + caracter
            posicion += 1
        return lexema

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
            "Léxico",
        )

    def _es_fin_linea(self):
        return self._actual() == "\n" or self._actual() == "\r"
