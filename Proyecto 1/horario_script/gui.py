


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from .analizador_lexico import AnalizadorLexico
import webbrowser
from .generador_reportes import GeneradorReportes
from .exportador_dot import exportar_dot
class VentanaHorarioScript:

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("HorarioScript - Analizador Lexico")
        self.raiz.geometry("900x650")

        self.ruta_archivo = None 

        self._crear_panel_carga()
        self._crear_panel_tokens()
        self._crear_panel_errores()
        self._crear_panel_reportes()
        self.ruta_archivo = None
        self.rutas_reportes = {}

    def _crear_panel_carga(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="x", padx=10, pady=8)

        self.boton_cargar = tk.Button(
            panel, text="Cargar archivo .hor", command=self.cargar_archivo
        )
        self.boton_cargar.pack(side="left")

        self.boton_analizar = tk.Button(
            panel, text="Analizar", state="disabled", command=self.analizar_archivo
        )
        self.boton_analizar.pack(side="left", padx=8)

        self.label_archivo = tk.Label(panel, text="Ningun archivo cargado", fg="gray")
        self.label_archivo.pack(side="left", padx=8)


    def _crear_panel_tokens(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(panel, text="Tokens reconocidos", font=("Arial", 10, "bold")).pack(anchor="w")

        columnas = ("num", "lexema", "tipo", "linea", "columna")
        self.tabla_tokens = ttk.Treeview(panel, columns=columnas, show="headings", height=8)

        self.tabla_tokens.heading("num", text="#")
        self.tabla_tokens.heading("lexema", text="Lexema")
        self.tabla_tokens.heading("tipo", text="Tipo")
        self.tabla_tokens.heading("linea", text="Linea")
        self.tabla_tokens.heading("columna", text="Columna")

        self.tabla_tokens.column("num", width=40, anchor="center")
        self.tabla_tokens.column("lexema", width=200)
        self.tabla_tokens.column("tipo", width=220)
        self.tabla_tokens.column("linea", width=60, anchor="center")
        self.tabla_tokens.column("columna", width=70, anchor="center")

        scroll_tokens = ttk.Scrollbar(panel, orient="vertical", command=self.tabla_tokens.yview)
        self.tabla_tokens.configure(yscrollcommand=scroll_tokens.set)

        self.tabla_tokens.pack(side="left", fill="both", expand=True)
        scroll_tokens.pack(side="left", fill="y")


    def _crear_panel_errores(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(panel, text="Errores lexicos", font=("Arial", 10, "bold")).pack(anchor="w")

        columnas = ("num", "lexema", "tipo_error", "linea", "columna", "descripcion")
        self.tabla_errores = ttk.Treeview(panel, columns=columnas, show="headings", height=6)

        self.tabla_errores.heading("num", text="#")
        self.tabla_errores.heading("lexema", text="Lexema invalido")
        self.tabla_errores.heading("tipo_error", text="Tipo de error")
        self.tabla_errores.heading("linea", text="Linea")
        self.tabla_errores.heading("columna", text="Columna")
        self.tabla_errores.heading("descripcion", text="Descripcion")

        self.tabla_errores.column("num", width=40, anchor="center")
        self.tabla_errores.column("lexema", width=140)
        self.tabla_errores.column("tipo_error", width=170)
        self.tabla_errores.column("linea", width=60, anchor="center")
        self.tabla_errores.column("columna", width=70, anchor="center")
        self.tabla_errores.column("descripcion", width=260)

        scroll_errores = ttk.Scrollbar(panel, orient="vertical", command=self.tabla_errores.yview)
        self.tabla_errores.configure(yscrollcommand=scroll_errores.set)

        self.tabla_errores.pack(side="left", fill="both", expand=True)
        scroll_errores.pack(side="left", fill="y")

    def _crear_panel_reportes(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="x", padx=10, pady=8)

        tk.Label(panel, text="Reportes:", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 8))

        self.boton_reporte1 = tk.Button(
        panel, text="Reporte 1: Horario semanal", state="disabled",
        command=lambda: self._abrir_reporte("horario"),)
        self.boton_reporte1.pack(side="left", padx=4)

        self.boton_reporte2 = tk.Button(
    panel, text="Reporte 2: Carga catedraticos", state="disabled",
    command=lambda: self._abrir_reporte("carga"),)
        self.boton_reporte2.pack(side="left", padx=4)

        self.boton_reporte3 = tk.Button(
            panel, text="Reporte 3: Estadistico general", state="disabled",
            command=lambda: self._abrir_reporte("estadistico"),
        )
        self.boton_reporte3.pack(side="left", padx=4)

        self.boton_dot = tk.Button(
            panel, text="Exportar diagrama AFD (.dot)", state="disabled",
            command=self._exportar_dot,
        )
        self.boton_dot.pack(side="left", padx=4)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo HorarioScript",
            filetypes=[("HorarioScript", "*.hor"), ("Todos los archivos", "*.*")],
        )

        if not ruta:
            return 

        self.ruta_archivo = ruta
        self.label_archivo.config(text=Path(ruta).name, fg="black")
        self.boton_analizar.config(state="normal")

    def analizar_archivo(self):
        if self.ruta_archivo is None:
            return
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                texto = archivo.read()
        except OSError as error:
            messagebox.showerror("Error al leer archivo", str(error))
            return
        analizador = AnalizadorLexico(texto)
        tokens = analizador.analizar()
        errores = analizador.errores
        self._poblar_tokens(tokens)
        self._poblar_errores(errores)
        self._generar_reportes(tokens)

    def _generar_reportes(self, tokens):
        carpeta_salida = Path(self.ruta_archivo).parent / "reportes"
        carpeta_salida.mkdir(exist_ok=True)

        generador = GeneradorReportes(tokens)

        ruta_horario = carpeta_salida / "reporte_horario.html"
        ruta_carga = carpeta_salida / "reporte_carga.html"
        generador.generar_reporte_horario(ruta_horario)
        generador.generar_reporte_carga(ruta_carga)
        ruta_estadistico = carpeta_salida / "reporte_estadistico.html"
        generador.generar_reporte_estadistico(ruta_estadistico)
        self.rutas_reportes["estadistico"] = ruta_estadistico
        self.boton_reporte3.config(state="normal")

        self.rutas_reportes["horario"] = ruta_horario
        self.rutas_reportes["carga"] = ruta_carga

        self.boton_reporte1.config(state="normal")
        self.boton_reporte2.config(state="normal")
        self.boton_reporte3.config(state="normal")
        self.boton_dot.config(state="normal")

    def _abrir_reporte(self, clave):
        ruta = self.rutas_reportes.get(clave)
        if ruta is None:
            return
        webbrowser.open(f"file://{Path(ruta).resolve()}")

    def _exportar_dot(self):
        carpeta_salida = Path(self.ruta_archivo).parent / "reportes"
        carpeta_salida.mkdir(exist_ok=True)
        ruta_dot = carpeta_salida / "afd_horarioscript.dot"
        exportar_dot(ruta_dot)
        messagebox.showinfo(
            "Diagrama AFD exportado",
            f"Archivo generado en:\n{ruta_dot}",
        )
    def _poblar_tokens(self, tokens):
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        for token in tokens:
            self.tabla_tokens.insert(
                "", "end",
                values=(token.numero, token.lexema, token.tipo, token.linea, token.columna),
            )
    def _poblar_errores(self, errores):
        self.tabla_errores.delete(*self.tabla_errores.get_children())
        for error in errores:
            self.tabla_errores.insert(
                "", "end",
                values=(error.numero, error.lexema, error.tipo, error.linea, error.columna, error.descripcion),
            )
if __name__ == "__main__":

    raiz = tk.Tk()
    app = VentanaHorarioScript(raiz)
    raiz.mainloop()