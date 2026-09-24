
## Cómo usar la aplicación

1. Ejecutar `python main.py`.
2. Presionar **Cargar archivo .hor** y seleccionar un archivo (ver ejemplos en `datos/`).
3. Presionar **Analizar** para ejecutar el motor léxico.
4. Revisar la tabla de tokens reconocidos y, si aplica, la tabla de errores léxicos.
5. Abrir cualquiera de los 3 reportes o exportar el diagrama del AFD desde los botones habilitados tras el análisis.

Instrucciones detalladas, con capturas de pantalla, en `Documentacion/Manual_de_Usuario_HorarioScript.pdf`.

## Tipos de token reconocidos

Palabras reservadas de bloque, elemento y relación; `CODIGO`, `CADENA`, `HORA`, `ENTERO`, `DIA`, `CATEGORIA`, `SIMBOLO` y `COMENTARIO_LINEA` — 11 tipos en total. Detalle completo en `Documentacion/Manual_Tecnico_HorarioScript.pdf`.

## Casos de prueba

10 casos documentados en `Documentacion/Casos_de_Prueba_HorarioScript.pdf`, cubriendo el archivo válido, los 5 tipos de error léxico, choques de horario (por catedrático y por aula), y 2 casos borde. Los archivos `.hor` de cada caso están en `datos/`.

## Restricciones técnicas cumplidas

- No se usa el módulo `re`.
- No se usan funciones de alto nivel de cadenas (`split`, `find`, etc.) para la tokenización principal; solo indexación carácter a carácter.
- No se usan generadores automáticos de analizadores léxicos (`ply` o similares).
- El AFD está implementado a mano, con estados y transiciones explícitas.