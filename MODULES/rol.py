class Rol:
    def __init__(self, descripcion, rol):
        self.__descripcion = descripcion
        self.__nombre = rol

    def esResponsableReparacion(self):
        if self.__nombre == "Responsable de Reparación":
            return True
        else:
            return False