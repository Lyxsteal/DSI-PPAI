def esEstadoActual(self, idSismografo):
        cambiosEstado = []
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM CambiosEstado 
            WHERE  idSismografo = ? AND fechaHoraFin IS NULL
            LIMIT 1''',(idSismografo,))
        actualCE = cursor.fetchone()
        conn.close()
        if actualCE is None:
            print(f"No se encontró cambio de estado actual para el sismógrafo {idSismografo}")
        return actualCE
def setFechaHoraFin(self, actualCE):
        tiempoFin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect('DATABASE/database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE CambiosEstado
            SET fechaHoraFin = ?
            WHERE idSismografo = ? AND fechaHoraInicio = ?''',(tiempoFin, actualCE[2], actualCE[0]))
        conn.commit()
        conn.close()
def crearMotivoFueraServicio(self, fechaActual, comentario_por_motivo, motivoTipo):
        try:
            for motivo, comentario in comentario_por_motivo.items():
                print(f'[DEBUG] Insertando MotivoFueraServicio con comentario: {comentario}, motivoTipo: {motivo}')
                conn = sqlite3.connect('DATABASE/database.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO MotivosFueraServicio(fechaInicio, comentario, descripcion) VALUES(?,?,?)''',(fechaActual, comentario, motivo))
                conn.commit()
                conn.close()
        except sqlite3.Error as e:
            print(f"[ERROR] Falló el INSERT en MotivosFueraServicio: {e}")
        self.__motivo = MotivoFueraServicio(comentario, motivoTipo)