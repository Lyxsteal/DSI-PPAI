class Rol:
    def __init__(self, rol):
        self.nombre = rol

    def esResponsableReparacion(self):
        return self.nombre == "Responsable de Reparación"