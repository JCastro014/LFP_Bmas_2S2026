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
    body {{ font-family: Arial, sans-serif; margin: 20px; color: #222; }}
    h1 {{ font-size: 20px; margin-bottom: 16px; color: #1f1f1f; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d9d9d9; padding: 8px 10px; text-align: left; vertical-align: top; }}
    th {{ background: #efefef; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    tr.confirmado td {{ background: #f4f9f4; }}
    tr.choque td {{ background: #fff2f0; font-weight: bold; }}
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
        carga_por_catedratico = {}
        for clase in self.clases:
            codigo_doc = clase["catedratico"]
            if codigo_doc is None or clase["inicio"] is None or clase["fin"] is None:
                continue
            duracion_horas = (_minutos(clase["fin"]) - _minutos(clase["inicio"])) / 60
            registro = carga_por_catedratico.setdefault(codigo_doc, {
                "horas": 0,
                "cursos": set(),
                "secciones": set(),
            })
            registro["horas"] += duracion_horas
            registro["cursos"].add(clase["curso"])
            registro["secciones"].add(clase["seccion"])

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
    body {{ font-family: Arial, sans-serif; margin: 20px; color: #222; }}
    h1 {{ font-size: 20px; margin-bottom: 16px; color: #1f1f1f; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d9d9d9; padding: 8px 10px; text-align: left; }}
    th {{ background: #f0f0f0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    tr:nth-child(even) td {{ background: #fafafa; }}
    tr.baja td {{ background: #edf6ff; }}
    tr.normal td {{ background: #f1f8f1; }}
    tr.alta td {{ background: #fff7eb; }}
    tr.saturada td {{ background: #fff0ef; }}
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

    def _nivel_carga(self, horas):
        if horas <= 4:
            return "BAJA", "baja"
        if horas <= 10:
            return "NORMAL", "normal"
        if horas <= 15:
            return "ALTA", "alta"
        return "SATURADA", "saturada"