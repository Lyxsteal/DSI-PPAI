import sqlite3
def estadoConsulta():
    conn = sqlite3.connect('DATABASE/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Estados")
    estados = cursor.fetchall()
    conn.close()
    return estados if estados else None