class Rol:
    def __init__(self, descripcion, rol):
        self.__descripcion = descripcion
        self.__nombre = rol

    def esResponsableReparacion(self):
        if self.__nombre is None:
            return False
        nombre_normalizado = self.__nombre.strip().lower()
        return nombre_normalizado in ("responsable de reparación", "responsable de reparacion")
