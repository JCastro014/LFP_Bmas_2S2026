
class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"Token({self.tipo}, '{self.valor}', linea={self.linea}, columna={self.columna})"


class Lexer:
    palabras_reservadas = {"if", "else", "while", "int", "return"}
    signos = {"(", ")", "{", "}", ";", ","}

    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.errores = []


    def avanzar(self):
        c = self.texto[self.pos]
        self.pos = self.pos + 1
        if c == "\n":
            self.linea = self.linea + 1
            self.columna = 1
        else:
            self.columna = self.columna + 1
        return c

    def peek(self):
        if self.pos < len(self.texto):
            return self.texto[self.pos]
        return None

    def analizar(self):

        while self.pos < len(self.texto):
            c = self.peek()


            if c == " " or c == "\t":
                self.avanzar()
                continue
            if c == "\n":
                self.avanzar()
                continue

            linea_inicio = self.linea
            columna_inicio = self.columna


            if c.isalpha() or c == "_":
                valor = ""
                while self.peek() is not None and (self.peek().isalnum() or self.peek() == "_"):
                    valor = valor + self.avanzar()

                if valor in self.palabras_reservadas:
                    tok = Token("PALABRA_RESERVADA", valor, linea_inicio, columna_inicio)
                else:
                    tok = Token("IDENTIFICADOR", valor, linea_inicio, columna_inicio)
                self.tokens.append(tok)
                continue

            if c.isdigit():
                valor = ""
                while self.peek() is not None and self.peek().isdigit():
                    valor = valor + self.avanzar()
                tok = Token("NUMERO", valor, linea_inicio, columna_inicio)
                self.tokens.append(tok)
                continue
            if c == "=" or c == "!" or c == "<" or c == ">":
                primero = self.avanzar()
                if self.peek() == "=":
                    segundo = self.avanzar()
                    valor = primero + segundo
                    tok = Token("OPERADOR", valor, linea_inicio, columna_inicio)
                    self.tokens.append(tok)
                else:
                    
                    if primero == "!":
                        msg = f"Error lexico: caracter '!' no reconocido en linea {linea_inicio}, columna {columna_inicio}"
                        self.errores.append(msg)
                    else:
                        tok = Token("OPERADOR", primero, linea_inicio, columna_inicio)
                        self.tokens.append(tok)
                continue

            if c == "+" or c == "-" or c == "*" or c == "/":
                valor = self.avanzar()
                tok = Token("OPERADOR", valor, linea_inicio, columna_inicio)
                self.tokens.append(tok)
                continue

            
            if c in self.signos:
                valor = self.avanzar()
                tok = Token("SIGNO", valor, linea_inicio, columna_inicio)
                self.tokens.append(tok)
                continue

            valor = self.avanzar()
            msg = f"Error lexico: caracter '{valor}' no reconocido en linea {linea_inicio}, columna {columna_inicio}"
            self.errores.append(msg)

    def imprimir_tokens(self):
        print(f"{'TIPO':<20}{'VALOR':<15}{'LINEA':<8}{'COLUMNA':<8}")
        print("-" * 50)
        for t in self.tokens:
            print(f"{t.tipo:<20}{t.valor:<15}{t.linea:<8}{t.columna:<8}")

    def imprimir_errores(self):
        if len(self.errores) == 0:
            print("No se encontraron errores lexicos")
        else:
            for e in self.errores:
                print(e)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("uso: python lexer.py archivo.txt")
        sys.exit(1)

    archivo = sys.argv[1]
    try:
        f = open(archivo, "r")
        contenido = f.read()
        f.close()
    except FileNotFoundError:
        print("Error: no se encontro el archivo", archivo)
        sys.exit(1)
    except Exception as e:
        print("Error leyendo el archivo:", e)
        sys.exit(1)

    lex = Lexer(contenido)
    lex.analizar()

    print("=== TABLA DE TOKENS ===")
    lex.imprimir_tokens()
    print()
    print("=== ERRORES LEXICOS ===")
    lex.imprimir_errores()