from Modelos.torneo import Torneo
from Logica.validador import validar_intento
from Logica.metricas import tiempo_promedio, validez_promedio, tasa_de_exito
from Logica.metricas import intentos_por_sudoku, intentos_por_jugador
from io_archivos.generador_de_reportes import generar_reporte_sudokus
from io_archivos.generador_de_reportes import generar_reporte_jugadores
from io_archivos.generador_de_reportes import generar_reporte_top10

def mostrar_menu():
    torneo = Torneo()
    opcion = ""

    while opcion != "8":
        print("==========================================")
        print(" TORNEO DE SUDOKU - NUMERIX")
        print("==========================================")
        print("1. Cargar archivo de sudokus")
        print("2. Cargar archivo de jugadores")
        print("3. Cargar archivo de intentos")
        print("4. Validar y calificar intentos")
        print("5. Generar Reporte: Resumen por Sudoku")
        print("6. Generar Reporte: Rendimiento por Jugador")
        print("7. Generar Reporte: Top 10 Mejores Tiempos")
        print("8. Salir")
        opcion = input("Seleccione una opcion: ")




        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo de sudokus")
            torneo.cargar_datos_sudokus(ruta)
            print("Sudkus cargados correctament")





        elif opcion == "2":
            ruta = input("Ingrese la ruta del archivo de jugadores: ")
            torneo.cargar_datos_jugadores(ruta)
            print("Jugadores cargados correctamente.")






        elif opcion == "3":
            ruta = input("Ingrese la ruta del archivo de intentos: ")
            torneo.cargar_datos_intentos(ruta)
            print(f"Se cargaron {len(torneo.intentos)} intentos de {ruta}.")







        elif opcion == "4":
            if len(torneo.intentos) == 0:
                print("Primero debe cargar los intentos (opcion 3).")
            else:
                for intento in torneo.intentos:
                    validar_intento(intento.tablero, intento)
                print("Intentos validados y calificados.")
                
                
                
                
                
        elif opcion == "5":
            print("Reporte de Resumen por Sudoku")
            if len(torneo.sudokus) == 0:
                print("Primero debe cargar los sudokus (opcion 1).")
            else:
                generar_reporte_sudokus(torneo.sudokus, torneo.intentos)
                print("Reporte generado: reportes/reporte_sudokus.html")
        elif opcion == "6":
            print("Reporte de Rendimiento por Jugador")
            if len(torneo.jugadores) == 0:
                print("Primero debe cargar los jugadores (opcion 2).")
            else:
                generar_reporte_jugadores(torneo.jugadores, torneo.intentos)
                print("Reporte generado: reportes/reporte_jugadores.html")
        elif opcion == "7":
            print("Reporte de Top 10 Mejores Tiempos")
            if len(torneo.intentos) == 0:
                print("Primero debe cargar y validar los intentos (opciones 3 y 4).")
            else:
                generar_reporte_top10(torneo.intentos)
                print("Reporte generado: reportes/reporte_top10.html")
        elif opcion == "8":
            print("Saliendo del sistema...")
        else:
            print("Opcion invalida, intente de nuevo.")