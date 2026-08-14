# Torneo de Sudoku — LFP Numerix

Sistema de consola en Python 3 para validar intentos de resolución de Sudoku, calcular métricas de desempeño de un torneo y generar reportes analíticos en HTML.

Proyecto de la práctica **"Torneo de Sudoku: Validación y Análisis de Partidas"** — Lenguajes Formales y de Programación, Universidad de San Carlos de Guatemala.

## Descripción

El sistema lee tres archivos de texto delimitados por comas (tableros, jugadores e intentos), representa cada uno como objetos mediante Programación Orientada a Objetos, valida cada intento contra las reglas del Sudoku (filas, columnas y cajas de 3x3) usando matrices, calcula métricas de desempeño y genera tres reportes en formato HTML.

## Requisitos

- Python 3.x
- No requiere librerías externas (solo módulos nativos de Python)

## Estructura del proyecto

```
Practica 1/
├── main.py
├── datos/
│   ├── sudokus.lfp
│   ├── jugadores.lfp
│   └── intentos.lfp
├── Modelos/
│   ├── tablero.py
│   ├── jugador.py
│   ├── intento.py
│   └── torneo.py
├── io_archivos/
│   ├── lector.py
│   └── generador_de_reportes.py
├── Logica/
│   ├── validador.py
│   └── metricas.py
├── Interfaz/
│   └── menu.py
└── reportes/
    ├── reporte_sudokus.html
    ├── reporte_jugadores.html
    └── reporte_top10.html
```

## Instrucciones de ejecución

1. Clonar el repositorio.
2. Abrir una terminal y ubicarse dentro de la carpeta `Practica 1` (la que contiene `main.py`):
   ```
   cd "Practica 1"
   ```
3. Ejecutar el programa:
   ```
   python main.py
   ```

**Importante:** el programa debe ejecutarse desde dentro de `Practica 1`, porque las rutas de los archivos de datos son relativas a esa ubicación.

## Ejemplo de uso

Al ejecutar `main.py` se muestra el menú principal:

```
==========================================
 TORNEO DE SUDOKU - NUMERIX
==========================================
1. Cargar archivo de sudokus
2. Cargar archivo de jugadores
3. Cargar archivo de intentos
4. Validar y calificar intentos
5. Generar Reporte: Resumen por Sudoku
6. Generar Reporte: Rendimiento por Jugador
7. Generar Reporte: Top 10 Mejores Tiempos
8. Salir
Seleccione una opcion:
```

Orden recomendado de uso:

1. Opción `1` — cargar `datos/sudokus.lfp`
2. Opción `2` — cargar `datos/jugadores.lfp`
3. Opción `3` — cargar `datos/intentos.lfp` (requiere que sudokus y jugadores ya estén cargados)
4. Opción `4` — validar y calificar los intentos cargados
5. Opciones `5`, `6`, `7` — generar los reportes HTML correspondientes en la carpeta `reportes/`
6. Opción `8` — salir

## Formato de los archivos de entrada

**`sudokus.lfp`** → `id_sudoku,dificultad,tablero` (cadena de 81 dígitos)
**`jugadores.lfp`** → `carnet,nombre,apellido,nivel`
**`intentos.lfp`** → `carnet,id_sudoku,solucion` (81 dígitos)`,tiempo_segundos,fecha`

## Reportes generados

Los tres reportes se guardan como archivos `.html` dentro de `reportes/` y se abren con cualquier navegador:

- `reporte_sudokus.html` — resumen por sudoku (intentos recibidos, tiempo promedio, tasa de éxito)
- `reporte_jugadores.html` — rendimiento por jugador (validez promedio, tiempo promedio, tableros resueltos perfectamente)
- `reporte_top10.html` — los 10 mejores tiempos entre los intentos resueltos correctamente

## Documentación adicional

- `Manual_Tecnico.docx` — estructura del programa, clases y lógica de validación matricial
- `Manual_Usuario.docx` — instrucciones de uso paso a paso
- Diagrama de flujo del proceso general
- Informe de desarrollo

## Autor

[Tu nombre] — Carnet [tu carnet] — Sección [tu sección]
