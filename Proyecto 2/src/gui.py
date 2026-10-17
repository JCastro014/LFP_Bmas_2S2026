import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

from .analizador_lexico import AnalizadorLexico
from .analizador_sintactico import AnalizadorSintactico
from .generador_html import GeneradorHTML
from .gestor_errores import GestorErrores


class VentanaMarkdownCheck:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("MarkdownCheck")
        self.raiz.geometry("1050x700")
        self.raiz.minsize(800, 550)

        self.ruta_archivo = None
        self.ruta_reporte = None
        self.arbol = None

        self._crear_panel_carga()

        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        self._crear_panel_tokens()
        self._crear_panel_errores()
        self._crear_panel_arbol()
        self._crear_panel_reportes()

        self.label_estado = tk.Label(
            self.raiz,
            text="Cargue un archivo .md para comenzar",
            anchor="w",
        )
        self.label_estado.pack(fill="x", padx=10, pady=8)

    def _crear_panel_carga(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="x", padx=10, pady=8)

        self.boton_cargar = tk.Button(
            panel,
            text="Cargar archivo .md",
            command=self.cargar_archivo,
        )
        self.boton_cargar.pack(side="left")

        self.label_archivo = tk.Label(
            panel,
            text="Ningún archivo cargado",
            fg="gray",
        )
        self.label_archivo.pack(side="left", padx=8)

        self.boton_analizar = tk.Button(
            panel,
            text="Analizar",
            state="disabled",
            command=self.analizar_archivo,
        )
        self.boton_analizar.pack(side="left", padx=8)

    def _crear_panel_tokens(self):
        panel = ttk.Frame(self.notebook)
        self.notebook.add(panel, text="Tokens")

        columnas = ("numero", "lexema", "tipo", "linea", "columna")
        self.tabla_tokens = ttk.Treeview(
            panel,
            columns=columnas,
            show="headings",
        )
        self.tabla_tokens.heading("numero", text="No.")
        self.tabla_tokens.heading("lexema", text="Lexema")
        self.tabla_tokens.heading("tipo", text="Tipo")
        self.tabla_tokens.heading("linea", text="Línea")
        self.tabla_tokens.heading("columna", text="Columna")

        self.tabla_tokens.column("numero", width=55, anchor="center")
        self.tabla_tokens.column("lexema", width=330)
        self.tabla_tokens.column("tipo", width=190)
        self.tabla_tokens.column("linea", width=70, anchor="center")
        self.tabla_tokens.column("columna", width=80, anchor="center")

        scroll = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.tabla_tokens.yview,
        )
        self.tabla_tokens.configure(yscrollcommand=scroll.set)
        self.tabla_tokens.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _crear_panel_errores(self):
        panel = ttk.Frame(self.notebook)
        self.notebook.add(panel, text="Errores")

        columnas = (
            "numero",
            "lexema",
            "tipo",
            "descripcion",
            "linea",
            "columna",
            "fase",
        )
        self.tabla_errores = ttk.Treeview(
            panel,
            columns=columnas,
            show="headings",
        )
        self.tabla_errores.heading("numero", text="No.")
        self.tabla_errores.heading("lexema", text="Lexema")
        self.tabla_errores.heading("tipo", text="Tipo")
        self.tabla_errores.heading("descripcion", text="Descripción")
        self.tabla_errores.heading("linea", text="Línea")
        self.tabla_errores.heading("columna", text="Columna")
        self.tabla_errores.heading("fase", text="Fase")

        self.tabla_errores.column("numero", width=50, anchor="center")
        self.tabla_errores.column("lexema", width=120)
        self.tabla_errores.column("tipo", width=180)
        self.tabla_errores.column("descripcion", width=360)
        self.tabla_errores.column("linea", width=65, anchor="center")
        self.tabla_errores.column("columna", width=75, anchor="center")
        self.tabla_errores.column("fase", width=100)

        scroll = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.tabla_errores.yview,
        )
        self.tabla_errores.configure(yscrollcommand=scroll.set)
        self.tabla_errores.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _crear_panel_arbol(self):
        panel = ttk.Frame(self.notebook)
        self.notebook.add(panel, text="Árbol sintáctico")

        self.texto_arbol = tk.Text(panel, wrap="none", state="disabled")
        scroll_vertical = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.texto_arbol.yview,
        )
        scroll_horizontal = ttk.Scrollbar(
            panel,
            orient="horizontal",
            command=self.texto_arbol.xview,
        )
        self.texto_arbol.configure(
            yscrollcommand=scroll_vertical.set,
            xscrollcommand=scroll_horizontal.set,
        )

        self.texto_arbol.pack(side="top", fill="both", expand=True)
        scroll_vertical.pack(side="right", fill="y")
        scroll_horizontal.pack(side="bottom", fill="x")

    def _crear_panel_reportes(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="x", padx=10, pady=5)

        tk.Label(panel, text="Reportes:").pack(side="left", padx=(0, 8))

        self.boton_reporte1 = tk.Button(
            panel,
            text="Abrir Reporte 1",
            state="disabled",
            command=self._abrir_reporte,
        )
        self.boton_reporte1.pack(side="left", padx=4)

        self.boton_reporte2 = tk.Button(
            panel,
            text="Reporte 2",
            state="disabled",
        )
        self.boton_reporte2.pack(side="left", padx=4)

        self.boton_reporte3 = tk.Button(
            panel,
            text="Reporte 3",
            state="disabled",
        )
        self.boton_reporte3.pack(side="left", padx=4)

        self.boton_exportar_arbol = tk.Button(
            panel,
            text="Exportar árbol",
            state="disabled",
        )
        self.boton_exportar_arbol.pack(side="left", padx=4)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo Markdown",
            filetypes=[
                ("Archivos Markdown", "*.md"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if ruta == "":
            return

        self.ruta_archivo = ruta
        self.ruta_reporte = None
        self.label_archivo.config(
            text=os.path.basename(ruta),
            fg="black",
        )
        self.boton_analizar.config(state="normal")
        self.boton_reporte1.config(state="disabled")
        self.label_estado.config(text="Archivo cargado. Presione Analizar.")

    def analizar_archivo(self):
        if self.ruta_archivo is None:
            return

        self.ruta_reporte = None
        self.boton_reporte1.config(state="disabled")
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                texto = archivo.read()
        except (OSError, UnicodeError) as error:
            messagebox.showerror("Error al leer archivo", str(error))
            self.label_estado.config(text="No se pudo leer el archivo.")
            return

        gestor_errores = GestorErrores()
        analizador_lexico = AnalizadorLexico(texto, gestor_errores)
        tokens = analizador_lexico.tokenizar()
        analizador_sintactico = AnalizadorSintactico(
            tokens,
            gestor_errores,
        )
        self.arbol = analizador_sintactico.parsear_documento()

        self._poblar_tokens(tokens)
        self._poblar_errores(gestor_errores.errores)
        self.texto_arbol.config(state="normal")
        self.texto_arbol.delete("1.0", "end")
        self.texto_arbol.insert("1.0", self.arbol.texto_arbol(0))
        self.texto_arbol.config(state="disabled")

        cantidad_errores = gestor_errores.cantidad()
        profundidad_listas = self.arbol.profundidad_maxima_listas()
        profundidad_citas = self.arbol.profundidad_maxima_citas()
        estado_profundidad = (
            " | Profundidad máxima de listas: "
            + str(profundidad_listas)
            + " | Profundidad máxima de citas: "
            + str(profundidad_citas)
        )

        if gestor_errores.hay_errores():
            self.label_estado.config(
                text=(
                    "Se encontraron "
                    + str(cantidad_errores)
                    + " errores"
                    + estado_profundidad
                )
            )
            return

        self.label_estado.config(
            text="Análisis correcto, 0 errores" + estado_profundidad
        )
        self.ruta_reporte = os.path.join(
            "reportes",
            "reporte1_documento.html",
        )
        try:
            os.makedirs("reportes", exist_ok=True)
            generador = GeneradorHTML(
                self.arbol,
                os.path.basename(self.ruta_archivo),
            )
            generador.guardar(self.ruta_reporte)
        except OSError as error:
            self.ruta_reporte = None
            messagebox.showerror("Error al guardar reporte", str(error))
            return

        self.boton_reporte1.config(state="normal")

    def _poblar_tokens(self, tokens):
        for fila in self.tabla_tokens.get_children():
            self.tabla_tokens.delete(fila)

        descripciones = {
            "FIN_LINEA": "(fin de línea)",
            "SALTO_PARRAFO": "(salto de párrafo)",
            "INDENT": "(indentación)",
            "DEDENT": "(fin de indentación)",
            "EOF": "(fin de archivo)",
        }

        for token in tokens:
            lexema = token.lexema
            if token.tipo in descripciones:
                lexema = descripciones[token.tipo]
            elif token.tipo == "TEXTO_LITERAL":
                lexema = self._texto_en_una_linea(lexema)

            self.tabla_tokens.insert(
                "",
                "end",
                values=(
                    token.numero,
                    lexema,
                    token.tipo,
                    token.linea,
                    token.columna,
                ),
            )

    def _texto_en_una_linea(self, texto):
        resultado = ""
        for caracter in texto:
            if caracter == "\n" or caracter == "\r":
                resultado += " "
            else:
                resultado += caracter
        return resultado

    def _poblar_errores(self, errores):
        for fila in self.tabla_errores.get_children():
            self.tabla_errores.delete(fila)

        for error in errores:
            self.tabla_errores.insert(
                "",
                "end",
                values=(
                    error.numero,
                    error.lexema,
                    error.tipo,
                    error.descripcion,
                    error.linea,
                    error.columna,
                    error.fase,
                ),
            )

    def _abrir_reporte(self):
        if self.ruta_reporte is None:
            return
        ruta_absoluta = os.path.abspath(self.ruta_reporte)
        ruta_navegador = "file:///" + ruta_absoluta.replace("\\", "/")
        webbrowser.open(ruta_navegador)
