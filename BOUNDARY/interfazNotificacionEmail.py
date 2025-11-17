from MODULES.ISuscriptoresOrden import ISuscriptoresOrden


class InterfazNotificacionEmail(ISuscriptoresOrden):
    def __init__(self):
        self.destinatarios = []

    def publicarNotificacion(self, idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios):
        if not self.destinatarios:
            return
        for mail in self.destinatarios:
            self.enviarMail(mail, idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios)
        print(f"Mails enviados. Un total de {len(self.destinatarios)} Mails.")

    def enviarMail(self, destinatario, idSismografo, nombreEstado, fechaHoraInicio, motivos, comentarios):
        motivos_str = self._formatear_lista(motivos)
        comentarios_str = self._formatear_comentarios(motivos, comentarios)
        print(f"Enviando email a {destinatario} -> Sismografo: {idSismografo}, Estado: {nombreEstado}, Fecha: {fechaHoraInicio}, Motivos: [{motivos_str}], Comentarios: [{comentarios_str}]")
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    def _formatear_lista(self, elementos):
        if not elementos:
            return ""
        if isinstance(elementos, (list, tuple)):
            return "///".join(str(e) for e in elementos)
        return str(elementos)

    def _formatear_comentarios(self, motivos, comentarios):
        if isinstance(comentarios, dict):
            if motivos:
                partes = [f"{motivo}: {comentarios.get(motivo, '')}" for motivo in motivos]
            else:
                partes = [f"{clave}: {valor}" for clave, valor in comentarios.items()]
            return "///".join(partes)
        if isinstance(comentarios, (list, tuple)):
            return "///".join(str(c) for c in comentarios)
        return str(comentarios) if comentarios else ""
