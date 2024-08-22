from app import conn, cur

tables = [
    """
    CREATE TABLE IF NOT EXISTS Ruoli (
        id SERIAL PRIMARY KEY,
        ruolo VARCHAR(255)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Vigilanti (
        id SERIAL PRIMARY KEY,
        nominativo VARCHAR(255),
        id_ruolo INTEGER REFERENCES Ruoli(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Appalti (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255),
        inizio DATE,
        fine DATE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Giorni (
        id SERIAL PRIMARY KEY,
        giorno VARCHAR(20)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Orari (
        id SERIAL PRIMARY KEY,
        id_appalto INTEGER REFERENCES Appalti(id),
        id_giorno INTEGER REFERENCES Giorni(id),
        inizio TIME,
        fine TIME
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Permessi (
        id SERIAL PRIMARY KEY,
        id_vigilante INTEGER REFERENCES Vigilanti(id),
        data DATE
    )
    """,
    """
        CREATE TABLE IF NOT EXISTS Assegnazioni (
            id SERIAL PRIMARY KEY,
            id_vigilante INTEGER REFERENCES Vigilanti(id),
            id_appalto INTEGER REFERENCES Appalti(id)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Preferenze (
            id SERIAL PRIMARY KEY,
            id_vigilante INTEGER REFERENCES Vigilanti(id),
            ore_lavoro iNTEGER,
            piu_turni BOOL,
            inizio TIME,
            fine TIME,
            riposi INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Servizi (
            id SERIAL PRIMARY KEY,
            id_vigilante INTEGER REFERENCES Vigilanti(id),
            id_appalto INTEGER REFERENCES Appalti(id),
            data DATE,
            inizio TIME,
            fine TIME
        )
    """
]

try:
    for query in tables:
        cur.execute(query)
    conn.commit()
except Exception as e:
    print(e)