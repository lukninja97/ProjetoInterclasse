CREATE DATABASE IF NOT EXISTS interclasse_db;

USE interclasse_db;

CREATE TABLE times (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    nome  VARCHAR(100) NOT NULL,
    turma   VARCHAR(20),
    responsavel   VARCHAR(100)
);

CREATE TABLE jogadores (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    nome     VARCHAR(100) NOT NULL,
    numero_camisa   INT,
    posicao  VARCHAR(50),
    time_id  INT,
    CONSTRAINT fk_jogador_time
        FOREIGN KEY (time_id) REFERENCES times (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE partidas (
    id              	INT AUTO_INCREMENT PRIMARY KEY,
    time_casa_id    	INT NOT NULL,
    time_visitante_id   INT NOT NULL,
    gols_casa       	INT DEFAULT 0,
    gols_visitante  	INT DEFAULT 0,
    data_partida    	DATE,
    CONSTRAINT fk_partida_time_casa
        FOREIGN KEY (time_casa_id) REFERENCES times (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_partida_time_visitante
        FOREIGN KEY (time_visitante_id) REFERENCES times (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
