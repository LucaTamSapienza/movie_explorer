import csv
import mariadb
import os
import re

def get_connection():
    """Restituisce una connessione al database MariaDB."""
    try:
        db_host = os.environ.get("DB_HOST", "127.0.0.1")
        db_port = int(os.environ.get("DB_PORT", 3307))
        db_user = os.environ.get("DB_USER", "user")
        db_password = os.environ.get("DB_PASSWORD", "pwd")
        db_name = os.environ.get("DB_NAME", "filmcatalogo")
        conn = mariadb.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mariadb.Error as e:
        print(f"Errore nella connessione al database: {e}")
        raise

def inserisci_dati_da_file(file_path: str):
    """Inserisce i dati da un file TSV nel database."""
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        with open(file_path, newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter='\t')

            for row in reader:
                titolo = row['Titolo'].strip()
                regista_nome = row['Regista'].strip()
                eta = int(row['Età_Autore'].strip())
                anno = int(row['Anno'].strip())
                genere = row['Genere'].strip()
                piattaforma_1 = row['Piattaforma_1'].strip() or None
                piattaforma_2 = row['Piattaforma_2'].strip() or None

                # same logic for ADD endpoint
                # 1. Inserisci o aggiorna il regista
                cur.execute("SELECT id FROM director WHERE nome = %s", (regista_nome,))
                regista = cur.fetchone()
                if regista:
                    regista_id = regista[0]
                    cur.execute(
                        "UPDATE director SET eta = %s WHERE id = %s",
                        (eta, regista_id)
                    )
                else:
                    cur.execute(
                        "INSERT INTO director (nome, eta) VALUES (%s, %s)",
                        (regista_nome, eta)
                    )
                    regista_id = cur.lastrowid

                # 2. Inserisci o aggiorna il film
                cur.execute("SELECT id FROM movies WHERE name = %s", (titolo,))
                film = cur.fetchone()
                if film:
                    film_id = film[0]
                    cur.execute(
                        "UPDATE movies SET year = %s, genere = %s, piattaforma_1 = %s, piattaforma_2 = %s WHERE id = %s",
                        (anno, genere, piattaforma_1, piattaforma_2, film_id)
                    )
                    # Elimina tutte le vecchie relazioni diretto per questo film
                    cur.execute(
                        "DELETE FROM diretto WHERE film_id = %s",
                        (film_id,)
                    )
                else:
                    cur.execute(
                        "INSERT INTO movies (name, year, genere, piattaforma_1, piattaforma_2) VALUES (%s, %s, %s, %s, %s)",
                        (titolo, anno, genere, piattaforma_1, piattaforma_2)
                    )
                    film_id = cur.lastrowid

                # 3. Inserisci la nuova relazione diretto
                cur.execute(
                    "INSERT INTO diretto (film_id, regista_id) VALUES (%s, %s)",
                    (film_id, regista_id)
                )

        conn.commit()
        print("✅ Dati inseriti correttamente!")

    except mariadb.Error as e:
        print(f"❌ Errore MariaDB: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def question_to_sql(question: str) -> str:
    """ 
    Converte una domanda in linguaggio naturale in una query SQL.
    """
    if match := re.match(r"Elenca i film del (\d{4})\.", question):
        year = match.group(1)
        return f"""
        SELECT m.name AS name, m.year, m.genere, m.piattaforma_1, m.piattaforma_2, d.nome AS director_nome, d.eta
        FROM movies m
        JOIN diretto di ON m.id = di.film_id
        JOIN director d ON di.regista_id = d.id
        WHERE m.year = {year}
        """
    elif match := re.match(r"Quali sono i registi presenti su Netflix\?", question):
        return """
        SELECT DISTINCT d.nome AS name, d.eta
        FROM director d
        JOIN diretto di ON d.id = di.regista_id
        JOIN movies m ON m.id = di.film_id
        WHERE m.piattaforma_1 = 'Netflix' OR m.piattaforma_2 = 'Netflix'
        """
    elif match := re.match(r"Elenca tutti i film di fantascienza\.", question):
        return """
        SELECT m.name AS name, m.year, m.genere, m.piattaforma_1, m.piattaforma_2, d.nome AS director_nome, d.eta
        FROM movies m
        JOIN diretto di ON m.id = di.film_id
        JOIN director d ON di.regista_id = d.id
        WHERE m.genere = 'Fantascienza'
        """
    elif match := re.match(r"Quali film sono stati fatti da un regista di almeno (\d+) anni\?", question):
        eta = match.group(1)
        return f"""
        SELECT m.name AS name, m.year, m.genere, m.piattaforma_1, m.piattaforma_2, d.nome AS director_nome, d.eta
        FROM movies m
        JOIN diretto di ON m.id = di.film_id
        JOIN director d ON di.regista_id = d.id
        WHERE d.eta >= {eta}
        """
    elif match := re.match(r"Quali registi hanno fatto più di un film\?", question):
        return """
        SELECT d.nome AS name, d.eta as eta, COUNT(*) as numero_film
        FROM director d
        JOIN diretto di ON d.id = di.regista_id
        GROUP BY d.nome
        HAVING COUNT(*) > 1
        """
    raise ValueError("Domanda non supportata.")

if __name__ == "__main__":
    import sys
    inserisci_dati_da_file(sys.argv[1])