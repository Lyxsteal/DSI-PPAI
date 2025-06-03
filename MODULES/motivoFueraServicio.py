from MODULES.motivosTipo import MotivoTipo
class MotivoFueraServicio:
    def __init__(self, comentario = None, motivoTipo:MotivoTipo=None):
        self.__comentario = comentario
        self.__motivoTipo = motivoTipo