from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from .utils import get_connection, question_to_sql

class SchemaSummary(BaseModel):
    """
    Modello per rappresentare una colonna di una tabella del database.
    """
    table_name: str
    table_column: str

class AddRequest(BaseModel):
    """
    Modello per rappresentare la richiesta di aggiunta di un film e regista.
    """
    data_line: str

app = FastAPI(title="Film Catalog API")

@app.get("/")
def root():
    """
    Restituisce un messaggio di benvenuto o stato del backend.
    return: Dizionario con stato e messaggio.
    """
    return {"status": "ok", "message": "Backend FilmCatalogo attivo"}

@app.get("/search/{question}")
def search(question: str):
    """
    Esegue una query SQL basata sulla domanda fornita.
    param: question (str): La domanda in linguaggio naturale.
    return: Lista di dizionari con i risultati della query.
    raise: HTTPException 422 se la domanda non è supportata.
    """
    try:
        query = question_to_sql(question)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    columns = [col[0] for col in cur.description]
    rows = cur.fetchall()

    # Determina item_type in base alle colonne
    if "genere" in columns:
        item_type = "film"
    elif "director_nome" in columns or "eta" in columns or "numero_film" in columns:
        item_type = "director"
    else:
        item_type = "item"

    response = []
    for row in rows:
        item = {
            "item_type": item_type,
            "properties": [
                {"property_name": col, "property_value": val}
                for col, val in zip(columns, row)
            ]
        }
        response.append(item)
    return response

@app.get("/schema_summary", response_model=list[SchemaSummary])
def schema_summary():
    """
    Restituisce un riepilogo dello schema del database.
    return: Lista di dizionari con nome tabella e colonna.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'filmcatalogo';")
    rows = cur.fetchall()
    return [{"table_name": table, "table_column": column} for table, column in rows]

@app.post("/add")
def add(request: AddRequest):
    """
    Aggiunge o aggiorna un film e il suo regista nel database.
    Se esiste già un film/regista con lo stesso nome, aggiorna tutti i campi.
    param: request (AddRequest): Oggetto contenente la stringa formattata con i dati.
    return: Dizionario con lo stato dell'operazione.
    raise: HTTPException 422 se il formato non è valido.
    """
    data_line = request.data_line
    parts = [part.strip() for part in data_line.split(",")]
    if len(parts) != 7:
        raise HTTPException(status_code=422, detail="Formato non valido. Servono 7 campi.")

    titolo, regista_nome, eta, anno, genere, piattaforma_1, piattaforma_2 = parts

    try:
        eta = int(eta)
        anno = int(anno)
    except ValueError:
        raise HTTPException(status_code=422, detail="Età e Anno devono essere numeri interi.")

    conn = get_connection()
    cur = conn.cursor()

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
    return {"status": "ok"}
