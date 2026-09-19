import tkinter as tk
from tkinter import ttk


class VentanaHorarioScript:


    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("HorarioScript - Analizador Lexico")
        self.raiz.geometry("900x650")

        self._crear_panel_carga()
        self._crear_panel_tokens()
        self._crear_panel_errores()
        self._crear_panel_reportes()
    def _crear_panel_carga(self):
        panel = tk.Frame(self.raiz)
        panel.pack(fill="x", padx=10, pady=8)

        self.boton_cargar = tk.Button(panel, text="Cargar archivo .hor")
        self.boton_cargar.pack(side="left")

        self.boton_analizar = tk.Button(panel, text="Analizar", state="disabled")
        self.boton_analizar.pack(side="left", padx=8)

        # Este label va a mostrar el nombre del archivo cargado (Dia 12)
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

        self.boton_reporte1 = tk.Button(panel, text="Reporte 1: Horario semanal", state="disabled")
        self.boton_reporte1.pack(side="left", padx=4)

        self.boton_reporte2 = tk.Button(panel, text="Reporte 2: Carga catedraticos", state="disabled")
        self.boton_reporte2.pack(side="left", padx=4)

        self.boton_reporte3 = tk.Button(panel, text="Reporte 3: Estadistico general", state="disabled")
        self.boton_reporte3.pack(side="left", padx=4)


if __name__ == "__main__":
    raiz = tk.Tk()
    app = VentanaHorarioScript(raiz)
    raiz.mainloop()