from pathlib import Path
from .estructura import extraer_cursos, extraer_catedraticos, extraer_aulas
from .detector_choques import extraer_clases, detectar_choques
ORDEN_DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]
def _minutos(hora_texto):
    horas = int(hora_texto[0:2])
    minutos = int(hora_texto[3:5])
    return horas * 60 + minutos
class GeneradorReportes:
    def __init__(self, tokens):
        self.cursos = extraer_cursos(tokens)
        self.catedraticos = extraer_catedraticos(tokens)
        self.aulas = extraer_aulas(tokens)
        self.clases = extraer_clases(tokens)
        self.choques = detectar_choques(self.clases)

        self.cursos_por_codigo = {c["codigo"]: c for c in self.cursos if c["codigo"]}
        self.catedraticos_por_codigo = {c["codigo"]: c for c in self.catedraticos if c["codigo"]}

        self._clases_en_choque = set()
        for choque in self.choques:
            self._clases_en_choque.add(id(choque["clase1"]))
            self._clases_en_choque.add(id(choque["clase2"]))
    def _nombre_curso(self, codigo):
        curso = self.cursos_por_codigo.get(codigo)
        return curso["nombre"] if curso else codigo
    def _nombre_catedratico(self, codigo):
        catedratico = self.catedraticos_por_codigo.get(codigo)
        return catedratico["nombre"] if catedratico else codigo
    def _en_choque(self, clase):
        return id(clase) in self._clases_en_choque
    def generar_reporte_horario(self, ruta_salida):
        clases_ordenadas = sorted(
            self.clases,
            key=lambda c: (
                ORDEN_DIAS.index(c["dia"]) if c["dia"] in ORDEN_DIAS else 99,
                _minutos(c["inicio"]) if c["inicio"] else 0,
            ),
        )

        filas = ""
        for clase in clases_ordenadas:
            estado = "CHOQUE DE HORARIO" if self._en_choque(clase) else "CONFIRMADO"
            clase_css = "choque" if self._en_choque(clase) else "confirmado"
            filas += f"""
            <tr class="{clase_css}">
                <td>{clase['dia'] or ''}</td>
                <td>{clase['inicio'] or ''} - {clase['fin'] or ''}</td>
                <td>{self._nombre_curso(clase['curso'])}</td>
                <td>{self._nombre_catedratico(clase['catedratico'])}</td>
                <td>{clase['aula'] or ''}</td>
                <td>{clase['seccion'] or ''}</td>
                <td>{estado}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Horario Semanal</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 18px; color: #111; }}
    h1 {{ font-size: 18px; margin-bottom: 12px; color: #111; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ border: 1px solid #bdbdbd; padding: 6px 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f3f3f3; font-size: 11px; text-transform: uppercase; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    tr.confirmado td {{ background: #f6f6f6; }}
    tr.choque td {{ background: #f7efef; font-weight: bold; }}
</style>
</head>
<body>
<h1>Reporte 1 — Horario Semanal</h1>
<table>
<tr><th>Día</th><th>Bloque</th><th>Curso</th><th>Catedrático</th><th>Aula</th><th>Sección</th><th>Estado</th></tr>
{filas}
</table>
</body>
</html>"""

        Path(ruta_salida).write_text(html, encoding="utf-8")

    def generar_reporte_carga(self, ruta_salida):
        carga_por_catedratico = self._calcular_carga_catedraticos()

        filas = ""
        for codigo_doc, datos in carga_por_catedratico.items():
            catedratico = self.catedraticos_por_codigo.get(codigo_doc, {})
            nombre = catedratico.get("nombre", codigo_doc)
            categoria = catedratico.get("categoria", "")
            horas = datos["horas"]
            nivel, clase_css = self._nivel_carga(horas)
            filas += f"""
            <tr class="{clase_css}">
                <td>{nombre}</td>
                <td>{codigo_doc}</td>
                <td>{categoria}</td>
                <td>{horas:.1f}</td>
                <td>{len(datos['cursos'])}</td>
                <td>{len(datos['secciones'])}</td>
                <td>{nivel}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Carga de Catedráticos</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 18px; color: #111; }}
    h1 {{ font-size: 18px; margin-bottom: 12px; color: #111; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ border: 1px solid #bdbdbd; padding: 6px 8px; text-align: left; }}
    th {{ background: #f3f3f3; font-size: 11px; text-transform: uppercase; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    tr.baja td {{ background: #f3f6fb; }}
    tr.normal td {{ background: #f4f7f4; }}
    tr.alta td {{ background: #faf5ee; }}
    tr.saturada td {{ background: #f9f0f0; }}
</style>
</head>
<body>
<h1>Reporte 2 — Carga de Catedráticos</h1>
<table>
<tr><th>Catedrático</th><th>Código</th><th>Categoría</th><th>Horas/semana</th><th>Cursos</th><th>Secciones</th><th>Nivel</th></tr>
{filas}
</table>
</body>
</html>"""

        Path(ruta_salida).write_text(html, encoding="utf-8")

    CAPACIDAD_SEMANAL_AULA_HORAS = 90  # 15 hrs/dia (06:00-21:00) x 6 dias (Lun-Sab)

    def _calcular_carga_catedraticos(self):
        carga = {}
        for clase in self.clases:
            codigo_doc = clase["catedratico"]
            if codigo_doc is None or clase["inicio"] is None or clase["fin"] is None:
                continue
            duracion_horas = (_minutos(clase["fin"]) - _minutos(clase["inicio"])) / 60
            registro = carga.setdefault(codigo_doc, {
                "horas": 0,
                "cursos": set(),
                "secciones": set(),
            })
            registro["horas"] += duracion_horas
            registro["cursos"].add(clase["curso"])
            registro["secciones"].add(clase["seccion"])
        return carga

    def _calcular_ocupacion_aulas(self):
        ocupacion = {}
        for clase in self.clases:
            codigo_aula = clase["aula"]
            if codigo_aula is None or clase["inicio"] is None or clase["fin"] is None:
                continue
            duracion_horas = (_minutos(clase["fin"]) - _minutos(clase["inicio"])) / 60
            registro = ocupacion.setdefault(codigo_aula, {"clases": 0, "horas": 0})
            registro["clases"] += 1
            registro["horas"] += duracion_horas
        return ocupacion

    def generar_reporte_estadistico(self, ruta_salida):
        carga = self._calcular_carga_catedraticos()
        ocupacion = self._calcular_ocupacion_aulas()

        total_cursos = len(self.cursos)
        total_catedraticos = len(self.catedraticos)
        total_aulas = len(self.aulas)
        total_clases = len(self.clases)
        total_choques = len(self.choques)

        catedratico_mayor_carga = max(carga.items(), key=lambda item: item[1]["horas"], default=None)
        aula_mayor_ocupacion = max(ocupacion.items(), key=lambda item: item[1]["horas"], default=None)

        promedio_horas = (
            sum(registro["horas"] for registro in carga.values()) / len(carga)
            if carga else 0
        )

        nombre_catedratico_top = (
            self._nombre_catedratico(catedratico_mayor_carga[0]) if catedratico_mayor_carga else "N/A"
        )
        nombre_aula_top = aula_mayor_ocupacion[0] if aula_mayor_ocupacion else "N/A"

        filas_aulas = ""
        for codigo_aula, datos in ocupacion.items():
            porcentaje = (datos["horas"] / self.CAPACIDAD_SEMANAL_AULA_HORAS) * 100
            filas_aulas += f"""
            <tr>
                <td>{codigo_aula}</td>
                <td>{datos['clases']}</td>
                <td>{datos['horas']:.1f}</td>
                <td>{porcentaje:.1f}%</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Estadistico General</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 20px; color: #111; }}
    h1 {{ font-size: 20px; margin-bottom: 16px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #bdbdbd; padding: 7px 8px; text-align: left; }}
    th {{ background: #f1f1f1; }}
</style>
</head>
<body>
<h1>Reporte 3 — Estadistico General</h1>
<p><strong>Cursos:</strong> {total_cursos}</p>
<p><strong>Catedraticos:</strong> {total_catedraticos}</p>
<p><strong>Aulas:</strong> {total_aulas}</p>
<p><strong>Clases:</strong> {total_clases}</p>
<p><strong>Choques:</strong> {total_choques}</p>
<p><strong>Promedio de horas por catedratico:</strong> {promedio_horas:.1f}</p>
<p><strong>Catedratico con mayor carga:</strong> {nombre_catedratico_top}</p>
<p><strong>Aula con mayor ocupacion:</strong> {nombre_aula_top}</p>

<h2>Ocupacion por aula</h2>
<table>
<tr><th>Aula</th><th>Clases asignadas</th><th>Horas/semana</th><th>% Ocupacion</th></tr>
{filas_aulas}
</table>
</body>
</html>"""

        Path(ruta_salida).write_text(html, encoding="utf-8")

    def _nivel_carga(self, horas):
        if horas <= 4:
            return "BAJA", "baja"
        if horas <= 10:
            return "NORMAL", "normal"
        if horas <= 15:
            return "ALTA", "alta"
        return "SATURADA", "saturada"