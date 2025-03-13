import sqlite3 as sql
BBDD = 'calculos.db'

def init_db():
    conn = sql.connect(BBDD)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    salario REAL,
                    edad INTEGER,
                    años_trabajados INTEGER,
                    resultado REAL
                )''')
    conn.commit()
    conn.close()
init_db()