 create table movimentacoes(
	id              	INT AUTO_INCREMENT PRIMARY KEY,
    jogador_id 			INT NOT NULL,
    time_origem_id    	INT NULL,
    time_destino_id     INT NULL,
	data_movimentacao 	DATETIME,

    CONSTRAINT fk_movimentacao_jogador
        FOREIGN KEY (jogador_id) REFERENCES jogadores(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_movimentacao_time_origem
        FOREIGN KEY (time_origem_id) REFERENCES times(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_movimentacao_time_destino
        FOREIGN KEY (time_destino_id) REFERENCES times(id)
        ON DELETE SET NULL
 );