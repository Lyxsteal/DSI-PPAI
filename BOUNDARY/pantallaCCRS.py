from MODULES.ISuscriptoresOrden import ISuscriptoresOrden


class PantallaCCRS(ISuscriptoresOrden):
    def __init__(self):
        pass

    def publicarNotificacion(self, idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios):
        self.mostrarActualizacion(idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios)

    def mostrarActualizacion(self, idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios):
        motivos_iterables = motivos if isinstance(motivos, list) else [motivos]
        for motivo in motivos_iterables:
            comentario = ""
            if isinstance(comentarios, dict):
                comentario = comentarios.get(motivo, "")
            elif isinstance(comentarios, (list, tuple)):
                comentario = comentarios[0] if comentarios else ""
            elif comentarios:
                comentario = comentarios
            print(f"Pantalla CCRS -> Sismografo: {idSismografo}, Estado: {nombreEstado}, Fecha/Hora: {fechaHoraInicio}, Motivo: {motivo}, Comentario: {comentario}")
            print("------------------------------------------------------------------------------------------------------------------------------------------------------------------")
