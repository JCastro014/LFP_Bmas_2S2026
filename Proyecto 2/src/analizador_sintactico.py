from .nodo_ast import NodoAST


class AnalizadorSintactico:
    def __init__(self, lista_tokens, gestor_errores):
        self.lista_tokens = lista_tokens
        self.gestor_errores = gestor_errores
        self.posicion = 0

    def _actual(self):
        if self.posicion >= len(self.lista_tokens):
            return self.lista_tokens[len(self.lista_tokens) - 1]
        return self.lista_tokens[self.posicion]

    def _avanzar(self):
        token = self._actual()
        if token.tipo != "EOF" and self.posicion < len(self.lista_tokens):
            self.posicion += 1
        return token

    def _consumir(self, tipo):
        token = self._actual()
        if token.tipo == tipo:
            self._avanzar()
            return NodoAST(token.tipo, token.lexema, token.linea, token.columna)

        self._registrar_error(
            token,
            "Se esperaba " + tipo + " y se encontró " + token.tipo,
        )
        self._recuperar()
        return NodoAST("ERROR_SINTACTICO", tipo, token.linea, token.columna)

    def _registrar_error(self, token, descripcion):
        self.gestor_errores.agregar(
            token.lexema,
            "ERROR_SINTACTICO",
            descripcion,
            token.linea,
            token.columna,
            "Sintáctico",
        )

    def _recuperar(self):
        while self._actual().tipo != "EOF":
            token = self._avanzar()
            if token.tipo == "FIN_LINEA" or token.tipo == "SALTO_PARRAFO":
                return

    def parsear_documento(self):
        nodo = NodoAST("documento")
        nodo.agregar_hijo(self.parsear_bloques())
        nodo.agregar_hijo(self._consumir("EOF"))
        return nodo

    def parsear_bloques(self):
        nodo = NodoAST("bloques")
        tipo = self._actual().tipo

        if tipo == "EOF" or tipo == "DEDENT":
            return nodo

        posicion_inicial = self.posicion
        nodo.agregar_hijo(self.parsear_bloque())
        if self.posicion == posicion_inicial and self._actual().tipo != "EOF":
            self._recuperar()
        nodo.agregar_hijo(self.parsear_bloques())
        return nodo

    def parsear_bloque(self):
        nodo = NodoAST("bloque")
        tipo = self._actual().tipo

        if tipo == "NUMERAL":
            nodo.agregar_hijo(self.parsear_encabezado())
        elif tipo == "REGLA_HORIZONTAL":
            nodo.agregar_hijo(self.parsear_regla())
        elif tipo == "CERCA_CODIGO":
            nodo.agregar_hijo(self.parsear_bloque_codigo())
        elif tipo == "VIÑETA":
            nodo.agregar_hijo(self.parsear_lista())
        elif tipo == "CITA":
            nodo.agregar_hijo(self.parsear_cita())
        elif tipo == "SALTO_PARRAFO":
            nodo.agregar_hijo(self._consumir("SALTO_PARRAFO"))
        elif tipo in ("NEGRITA", "CURSIVA", "CODIGO_INLINE", "TEXTO"):
            nodo.agregar_hijo(self.parsear_parrafo())
        else:
            token = self._actual()
            self._registrar_error(
                token,
                "No se reconoce el inicio de un bloque: " + tipo,
            )
            self._recuperar()

        return nodo

    def parsear_encabezado(self):
        nodo = NodoAST("encabezado")
        nodo.agregar_hijo(self._consumir("NUMERAL"))
        nodo.agregar_hijo(self.parsear_en_linea())
        nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        return nodo

    def parsear_regla(self):
        nodo = NodoAST("regla")
        nodo.agregar_hijo(self._consumir("REGLA_HORIZONTAL"))
        nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        return nodo

    def parsear_lista(self):
        nodo = NodoAST("lista")
        nodo.agregar_hijo(self.parsear_item_lista())
        nodo.agregar_hijo(self.parsear_lista_resto())
        return nodo

    def parsear_lista_resto(self):
        nodo = NodoAST("lista_resto")
        if self._actual().tipo == "VIÑETA":
            nodo.agregar_hijo(self.parsear_item_lista())
            nodo.agregar_hijo(self.parsear_lista_resto())
        return nodo

    def parsear_item_lista(self):
        nodo = NodoAST("item_lista")
        nodo.agregar_hijo(self._consumir("VIÑETA"))
        nodo.agregar_hijo(self.parsear_en_linea())
        nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        nodo.agregar_hijo(self.parsear_sublista_opt())
        return nodo

    def parsear_sublista_opt(self):
        nodo = NodoAST("sublista_opt")
        if self._actual().tipo == "INDENT":
            nodo.agregar_hijo(self._consumir("INDENT"))
            nodo.agregar_hijo(self.parsear_lista())
            nodo.agregar_hijo(self._consumir("DEDENT"))
        return nodo

    def parsear_cita(self):
        nodo = NodoAST("cita")
        nodo.agregar_hijo(self.parsear_linea_cita())
        nodo.agregar_hijo(self.parsear_cita_resto())
        return nodo

    def parsear_cita_resto(self):
        nodo = NodoAST("cita_resto")
        if self._actual().tipo == "CITA":
            nodo.agregar_hijo(self.parsear_linea_cita())
            nodo.agregar_hijo(self.parsear_cita_resto())
        return nodo

    def parsear_linea_cita(self):
        nodo = NodoAST("linea_cita")
        nodo.agregar_hijo(self._consumir("CITA"))
        nodo.agregar_hijo(self.parsear_cuerpo_cita())
        return nodo

    def parsear_cuerpo_cita(self):
        nodo = NodoAST("cuerpo_cita")
        if self._actual().tipo == "CITA":
            nodo.agregar_hijo(self._consumir("CITA"))
            nodo.agregar_hijo(self.parsear_cuerpo_cita())
        else:
            nodo.agregar_hijo(self.parsear_en_linea())
            nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        return nodo

    def parsear_parrafo(self):
        nodo = NodoAST("parrafo")
        nodo.agregar_hijo(self.parsear_linea_texto())
        nodo.agregar_hijo(self.parsear_parrafo_resto())
        return nodo

    def parsear_parrafo_resto(self):
        nodo = NodoAST("parrafo_resto")
        if self._actual().tipo in (
            "NEGRITA",
            "CURSIVA",
            "CODIGO_INLINE",
            "TEXTO",
        ):
            nodo.agregar_hijo(self.parsear_linea_texto())
            nodo.agregar_hijo(self.parsear_parrafo_resto())
        return nodo

    def parsear_linea_texto(self):
        nodo = NodoAST("linea_texto")
        nodo.agregar_hijo(self.parsear_elemento())
        nodo.agregar_hijo(self.parsear_en_linea())
        nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        return nodo

    def parsear_bloque_codigo(self):
        nodo = NodoAST("bloque_codigo")
        nodo.agregar_hijo(self._consumir("CERCA_CODIGO"))
        nodo.agregar_hijo(self.parsear_lenguaje_opt())
        nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        nodo.agregar_hijo(self.parsear_contenido_cod())
        nodo.agregar_hijo(self._consumir("CERCA_CODIGO"))
        nodo.agregar_hijo(self._consumir("FIN_LINEA"))
        return nodo

    def parsear_lenguaje_opt(self):
        nodo = NodoAST("lenguaje_opt")
        if self._actual().tipo == "LENGUAJE":
            nodo.agregar_hijo(self._consumir("LENGUAJE"))
        return nodo

    def parsear_contenido_cod(self):
        nodo = NodoAST("contenido_cod")
        if self._actual().tipo == "TEXTO_LITERAL":
            nodo.agregar_hijo(self._consumir("TEXTO_LITERAL"))
        return nodo

    def parsear_en_linea(self):
        nodo = NodoAST("en_linea")
        if self._actual().tipo in (
            "NEGRITA",
            "CURSIVA",
            "CODIGO_INLINE",
            "TEXTO",
        ):
            nodo.agregar_hijo(self.parsear_elemento())
            nodo.agregar_hijo(self.parsear_en_linea())
        return nodo

    def parsear_elemento(self):
        nodo = NodoAST("elemento")
        tipo = self._actual().tipo

        if tipo == "NEGRITA":
            nodo.agregar_hijo(self.parsear_negrita())
        elif tipo == "CURSIVA":
            nodo.agregar_hijo(self.parsear_cursiva())
        elif tipo == "CODIGO_INLINE":
            nodo.agregar_hijo(self.parsear_codigo_inline())
        elif tipo == "TEXTO":
            nodo.agregar_hijo(self._consumir("TEXTO"))
        else:
            token = self._actual()
            self._registrar_error(
                token,
                "Se esperaba un elemento en línea y se encontró " + tipo,
            )
            self._recuperar()
            nodo.agregar_hijo(
                NodoAST("ERROR_SINTACTICO", tipo, token.linea, token.columna)
            )

        return nodo

    def parsear_negrita(self):
        nodo = NodoAST("negrita")
        nodo.agregar_hijo(self._consumir("NEGRITA"))
        nodo.agregar_hijo(self.parsear_en_negrita())
        nodo.agregar_hijo(self._consumir("NEGRITA"))
        return nodo

    def parsear_en_negrita(self):
        nodo = NodoAST("en_negrita")
        if self._actual().tipo in ("CURSIVA", "CODIGO_INLINE", "TEXTO"):
            nodo.agregar_hijo(self.parsear_elem_neg())
            nodo.agregar_hijo(self.parsear_en_negrita())
        return nodo

    def parsear_elem_neg(self):
        nodo = NodoAST("elem_neg")
        tipo = self._actual().tipo

        if tipo == "CURSIVA":
            nodo.agregar_hijo(self.parsear_cursiva())
        elif tipo == "CODIGO_INLINE":
            nodo.agregar_hijo(self.parsear_codigo_inline())
        elif tipo == "TEXTO":
            nodo.agregar_hijo(self._consumir("TEXTO"))
        else:
            token = self._actual()
            self._registrar_error(
                token,
                "Se esperaba un elemento de negrita y se encontró " + tipo,
            )
            self._recuperar()
            nodo.agregar_hijo(
                NodoAST("ERROR_SINTACTICO", tipo, token.linea, token.columna)
            )

        return nodo

    def parsear_cursiva(self):
        nodo = NodoAST("cursiva")
        nodo.agregar_hijo(self._consumir("CURSIVA"))
        nodo.agregar_hijo(self.parsear_en_cursiva())
        nodo.agregar_hijo(self._consumir("CURSIVA"))
        return nodo

    def parsear_en_cursiva(self):
        nodo = NodoAST("en_cursiva")
        if self._actual().tipo in ("NEGRITA", "CODIGO_INLINE", "TEXTO"):
            nodo.agregar_hijo(self.parsear_elem_curs())
            nodo.agregar_hijo(self.parsear_en_cursiva())
        return nodo

    def parsear_elem_curs(self):
        nodo = NodoAST("elem_curs")
        tipo = self._actual().tipo

        if tipo == "NEGRITA":
            nodo.agregar_hijo(self.parsear_negrita())
        elif tipo == "CODIGO_INLINE":
            nodo.agregar_hijo(self.parsear_codigo_inline())
        elif tipo == "TEXTO":
            nodo.agregar_hijo(self._consumir("TEXTO"))
        else:
            token = self._actual()
            self._registrar_error(
                token,
                "Se esperaba un elemento de cursiva y se encontró " + tipo,
            )
            self._recuperar()
            nodo.agregar_hijo(
                NodoAST("ERROR_SINTACTICO", tipo, token.linea, token.columna)
            )

        return nodo

    def parsear_codigo_inline(self):
        nodo = NodoAST("codigo_inline")
        nodo.agregar_hijo(self._consumir("CODIGO_INLINE"))
        nodo.agregar_hijo(self._consumir("TEXTO_LITERAL"))
        nodo.agregar_hijo(self._consumir("CODIGO_INLINE"))
        return nodo
