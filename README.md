# Movie Explorer

Movie Explorer è un progetto web che permette di gestire e consultare un catalogo di film e registi, con funzionalità di ricerca avanzata in linguaggio naturale. Il sistema è composto da un backend (FastAPI + MariaDB) e un frontend (FastAPI + Jinja2), orchestrati tramite Docker Compose.

## Funzionalità

- Ricerca di film e registi tramite domande in linguaggio naturale
- Visualizzazione dettagliata di film, registi e piattaforme
- Aggiunta di nuovi film e registi
- Visualizzazione dello schema del database

## Struttura del progetto

- `backend/`: codice e dati del backend (API, popolamento database)
- `frontend/`: codice del frontend (interfaccia web, template, static)
- `mariadb_init/`: script di inizializzazione del database
- `docker-compose.yaml`: orchestrazione dei servizi
- `mariadb_data/`: dati persistenti del database (non versionati)

## Requisiti

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Avvio rapido

1. Clona il repository:
    ```sh
    git clone <repo-url>
    cd esonero
    ```

2. Avvia tutti i servizi (backend, frontend, database) con:
    ```sh
    docker-compose up --build
    ```

3. Accedi al frontend all’indirizzo:  
   [http://localhost:8001](http://localhost:8001)

## Comandi utili

- **Ricostruire i container:**  
  ```sh
    docker-compose up --build
    ```
- **distruggere i container:**      
    ```sh
    docker-compose down -v
    ```