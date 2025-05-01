CREATE DATABASE IF NOT EXISTS filmcatalogo;
USE filmcatalogo;

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    year INT,
    genere VARCHAR(100),
    piattaforma_1 VARCHAR(100),
    piattaforma_2 VARCHAR(100)
);

CREATE TABLE director (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) UNIQUE NOT NULL,
    eta INT
);

CREATE TABLE diretto (
    film_id INT,
    regista_id INT,
    PRIMARY KEY (film_id, regista_id),
    FOREIGN KEY (film_id) REFERENCES movies(id),
    FOREIGN KEY (regista_id) REFERENCES director(id)
);