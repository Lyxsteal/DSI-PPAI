class MotivoTipo:
    def __init__(self, descripcion):
        self.__descripcion = descripcion[0]
    def getDescripcion(self):
        return self.__descripcion
    def __str__(self):
        return self.__descripcion