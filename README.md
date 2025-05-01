# Movie Explorer

Movie Explorer is a web project that allows you to manage and browse a catalog of movies and directors, with advanced natural language search functionality. The system consists of a backend (FastAPI + MariaDB) and a frontend (FastAPI + Jinja2), orchestrated via Docker Compose.

## Features

- Search for movies and directors using natural language queries
- Detailed view of movies, directors, and platforms
- Add new movies and directors
- View the database schema

## Project Structure

- `backend/`: backend code and data (API, database population)
- `frontend/`: frontend code (web interface, templates, static files)
- `mariadb_init/`: database initialization scripts
- `docker-compose.yaml`: service orchestration
- `mariadb_data/`: persistent database data (not versioned)

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Quick Start

1. Clone the repository:
    ```sh
    git clone <repo-url>
    cd esonero
    ```

2. Start all services (backend, frontend, database) with:
    ```sh
    docker-compose up --build
    ```

3. Access the frontend at:  
   [http://localhost:8001](http://localhost:8001)

## Useful Commands

- **Rebuild containers:**  
  ```sh
    docker-compose up --build
    ```
- **Destroy containers:**      
    ```sh
    docker-compose down -v
    ```