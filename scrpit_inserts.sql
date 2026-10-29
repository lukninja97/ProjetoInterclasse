
-- 10 times
INSERT INTO times (nome, turma, responsavel) VALUES
('Águias FC', '3A', 'Carlos Silva'),
('Tigres FC', '3B', 'Mariana Souza'),
('Leões FC', '4A', 'Rafael Oliveira'),
('Falcões FC', '4B', 'Juliana Santos'),
('Panteras FC', '5A', 'Bruno Costa'),
('Lobos FC', '5B', 'Fernanda Lima'),
('Dragões FC', '6A', 'Lucas Almeida'),
('Cobras FC', '6B', 'Patrícia Rocha'),
('Gaviões FC', '7A', 'André Martins'),
('Rinocerontes FC', '7B', 'Camila Ferreira');


-- 6 jogadores por time
INSERT INTO jogadores (nome, numero_camisa, posicao, time_id) VALUES

-- Águias FC - time_id 1
('João Pedro', 1, 'Goleiro', 1),
('Miguel Santos', 4, 'Zagueiro', 1),
('Lucas Mendes', 7, 'Meia', 1),
('Gabriel Costa', 10, 'Atacante', 1),
('Pedro Henrique', 8, 'Meia', 1),
('Matheus Lima', 9, 'Atacante', 1),

-- Tigres FC - time_id 2
('Arthur Souza', 1, 'Goleiro', 2),
('Enzo Martins', 3, 'Zagueiro', 2),
('Rafael Gomes', 6, 'Volante', 2),
('Davi Oliveira', 10, 'Meia', 2),
('Bernardo Alves', 7, 'Atacante', 2),
('Gustavo Rocha', 11, 'Atacante', 2),

-- Leões FC - time_id 3
('Felipe Santos', 1, 'Goleiro', 3),
('Thiago Costa', 2, 'Lateral', 3),
('Henrique Silva', 5, 'Volante', 3),
('Leonardo Lima', 8, 'Meia', 3),
('Vinícius Souza', 9, 'Atacante', 3),
('Caio Ferreira', 10, 'Atacante', 3),

-- Falcões FC - time_id 4
('Bruno Mendes', 1, 'Goleiro', 4),
('Eduardo Santos', 4, 'Zagueiro', 4),
('Diego Oliveira', 6, 'Volante', 4),
('Murilo Costa', 7, 'Meia', 4),
('Samuel Alves', 9, 'Atacante', 4),
('Rodrigo Lima', 11, 'Atacante', 4),

-- Panteras FC - time_id 5
('Alexandre Souza', 1, 'Goleiro', 5),
('Marcelo Silva', 3, 'Zagueiro', 5),
('Renan Costa', 5, 'Volante', 5),
('Wesley Santos', 8, 'Meia', 5),
('Igor Oliveira', 10, 'Atacante', 5),
('Nicolas Ferreira', 9, 'Atacante', 5),

-- Lobos FC - time_id 6
('Victor Hugo', 1, 'Goleiro', 6),
('André Luiz', 2, 'Lateral', 6),
('João Vitor', 4, 'Zagueiro', 6),
('Ryan Martins', 6, 'Volante', 6),
('Cauã Souza', 7, 'Meia', 6),
('Heitor Lima', 10, 'Atacante', 6),

-- Dragões FC - time_id 7
('Daniel Alves', 1, 'Goleiro', 7),
('Guilherme Costa', 3, 'Zagueiro', 7),
('Nathan Silva', 5, 'Volante', 7),
('Luiz Fernando', 8, 'Meia', 7),
('Yuri Santos', 9, 'Atacante', 7),
('Arthur Lima', 11, 'Atacante', 7),

-- Cobras FC - time_id 8
('Cristian Souza', 1, 'Goleiro', 8),
('Alan Martins', 2, 'Lateral', 8),
('Kevin Oliveira', 4, 'Zagueiro', 8),
('Jonathan Costa', 6, 'Volante', 8),
('Erick Santos', 10, 'Meia', 8),
('Vitor Rocha', 9, 'Atacante', 8),

-- Gaviões FC - time_id 9
('Fernando Silva', 1, 'Goleiro', 9),
('Ricardo Mendes', 3, 'Zagueiro', 9),
('Marcelo Oliveira', 5, 'Volante', 9),
('Fábio Santos', 7, 'Meia', 9),
('Márcio Lima', 9, 'Atacante', 9),
('Renato Costa', 11, 'Atacante', 9),

-- Rinocerontes FC - time_id 10
('Alex Silva', 1, 'Goleiro', 10),
('Diego Martins', 2, 'Lateral', 10),
('Roberto Souza', 4, 'Zagueiro', 10),
('Paulo Henrique', 6, 'Volante', 10),
('Júlio César', 8, 'Meia', 10),
('Gustavo Lima', 10, 'Atacante', 10);