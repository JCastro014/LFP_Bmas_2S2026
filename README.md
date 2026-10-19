# MarkdownCheck

Proyecto 2 de Lenguajes Formales y de Programación, Sección B+, Segundo Semestre 2026.
Universidad de San Carlos de Guatemala, Facultad de Ingeniería.

**Autor:** Josué Eliú Castro Sosa, carné 202405110

## Descripción

MarkdownCheck es un analizador léxico-sintáctico hecho en Python que lee archivos `.md`
(un subconjunto de Markdown) y los traduce a HTML.

- El **analizador léxico** es un AFD implementado a mano (sin el módulo `re`).
- El **analizador sintáctico** es un parser descendente recursivo implementado a mano,
  con una función por cada símbolo no terminal de la gramática de la Tarea 4.
- Del parser sale un **árbol de derivación (AST)**, y el HTML se genera recorriendo ese árbol.
- Registra errores léxicos y sintácticos con su posición y sigue analizando (modo pánico).

## Requisitos

- Python 3.10 o superior.
- Solo biblioteca estándar (Tkinter viene incluido con Python). No hay dependencias que instalar.
- Opcional: Graphviz, solo si se quiere convertir `arbol.dot` en imagen.

## Cómo ejecutar

Desde la carpeta `Proyecto 2`:

```
python main.py
```

Se abre la interfaz gráfica. Pasos básicos:

1. Cargar un archivo `.md` (hay ejemplos en `examples/`).
2. Ejecutar el análisis.
3. Revisar la tabla de tokens y la tabla de errores.
4. Si no hay errores, abrir los 3 reportes HTML.

También se puede probar con un archivo desde consola:

```
python main.py examples/ejemplo_valido.md
```

Pruebas, también desde la raíz de `Proyecto 2`:

```
python -m tests.prueba_lexico
python -m tests.prueba_sintactico
```

## Sintaxis Markdown soportada

- Encabezados `#` a `######`
- Párrafos
- **Negrita** (`**`), *cursiva* (`*`) y `código en línea`
- Listas no ordenadas anidadas (3 o más niveles, 2 espacios por nivel)
- Citas `>` anidadas (2 o más niveles)
- Bloques de código con ``` (contenido literal)
- Regla horizontal `---`

## Salidas generadas

| Salida | Descripción |
|---|---|
| Reporte 1 | Documento HTML renderizado desde el AST |
| Reporte 2 | Estadísticas del documento |
| Reporte 3 | Tabla de contenido con enlaces internos |
| `arbol.dot` | Árbol de derivación en Graphviz |

Los reportes solo se generan cuando el análisis termina sin errores.

## Estructura del repositorio

```
Proyecto 2/
├── main.py              arranque del programa
├── README.md
├── .gitignore
├── src/                 código fuente (lexer, parser, AST, generadores, GUI)
├── tests/               pruebas
├── examples/            archivos .md de ejemplo
└── docs/                Manual Técnico, Manual de Usuario y Casos de Prueba (PDF)
```

## Documentación

En la carpeta `docs/`:

- Manual Técnico (PDF)
- Manual de Usuario (PDF)
- Casos de Prueba (PDF)

## Restricciones cumplidas

- No se usa el módulo `re` para tokenizar.
- No se usan librerías de parsing ni de conversión Markdown.
- El HTML se genera recorriendo el AST, no por sustitución de texto.