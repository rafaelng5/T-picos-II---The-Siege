-- Criação do banco de dados
CREATE DATABASE jogo;

-- Usar o banco de dados
USE jogo;

-- Criação da tabela jogador
CREATE TABLE jogador (
    nome VARCHAR(100) PRIMARY KEY
);

-- Criação da tabela fase
CREATE TABLE fase (
    nome VARCHAR(100) PRIMARY KEY
);

-- Criação da tabela pontuacao
CREATE TABLE pontuacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_jogador INT,
    id_fase INT,
    pontuacao INT NOT NULL,
    tempo TIME NOT NULL,
    FOREIGN KEY (id_jogador) REFERENCES jogador(nome),
    FOREIGN KEY (id_fase) REFERENCES fase(nome)
);



