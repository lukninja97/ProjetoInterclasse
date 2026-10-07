from flask import flash
from sqlalchemy import select
from sqlalchemy.dialects.mssql.information_schema import columns
from sqlalchemy.exc import SQLAlchemyError

from database import Jogador, db_session, Time


def select_todos():
    # 1 - Montar o select
    jogadores_sql = select(Jogador)
    # 2 - Executar o select
    jogadores = db_session.execute(jogadores_sql).all()
    print(jogadores)

    return jogadores

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
        db_session.add(jogador)
        db_session.commit()
        flash("Jogador criado com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")

select_todos()