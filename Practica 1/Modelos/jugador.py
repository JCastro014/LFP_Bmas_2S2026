class Jugador:
    def __init__(self, carnet, nombre, apellido, nivel):
        self.carnet = int(carnet)
        self.nombre = nombre
        self.apellido = apellido
        self.nivel = nivel
    def __str__(self):
        return f"Jugador: {self.carnet}, Nombre: {self.nombre}, Apellido: {self.apellido}, Nivel: {self.nivel}"