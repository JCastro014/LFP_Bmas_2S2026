# Tabla de transiciones del AFD (Tarea 3)

| Estado actual | Entrada              | Estado siguiente |
|----------------|----------------------|-------------------|
| q0             | letra o _            | q1                |
| q1             | letra, digito o _    | q1                |
| q1             | otro                 | q0 (token emitido)|
| q0             | digito                | q2                |
| q2             | digito                | q2                |
| q2             | otro                  | q0 (token emitido)|
| q0             | = ! < >               | q3                |
| q3             | =                     | q4 (token emitido)|
| q3             | otro (si no era !)    | q5 (token emitido)|
| q3             | otro (si era !)       | qerr              |
| q0             | + - * /               | q5 (token emitido)|
| q0             | ( ) { } ; ,           | q6 (token emitido)|
| q0             | espacio, tab, salto   | q0                |
| q0             | cualquier otro        | qerr              |
