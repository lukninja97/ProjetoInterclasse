from functools import wraps
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, render_template, request, redirect, url_for, flash
from banco import tabela_time, tabela_jogador, tabela_partida, tabela_movimentacao
from database import db_session, Usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
# secret_key aqui apenas em momento de criação, em produção deve ser protegida
app.secret_key = "chave-secreta-interclasse-2026"

# Configuração Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar"


# Prevenir gargalo "too many connections"
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# carregar informações do usuario logado
@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))

def roles_required(*papeis_permitidos):
    '''
        Decorator para restringir acesso
        baseado no papel do usuario logado
    '''
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.papel not in papeis_permitidos:
                flash("Acesso negado:Você não tem permissão para acessar esta página", 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Interface de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario_sql = select(Usuario).where(Usuario.email == email)
        usuario_resultado = db_session.execute(usuario_sql).scalar()

        if not usuario_resultado:
            flash('Falha na autenticação: E-mail não encontrado', 'error')
            return redirect(url_for('login'))

        if usuario_resultado and usuario_resultado.check_password(senha):
            login_user(usuario_resultado)
            return redirect(url_for('dashboard'))
        else:
            flash('Falha na autenticação: Senha incorreta', 'error')

    return render_template(
        "login.html",
        registro= request.args.get("registro") == 'True'
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not nome and not email and not senha:
            flash('Preencher todos os campos', 'error')
            return redirect(url_for('registro'))
        usuario_sql = select(Usuario).where(Usuario.email == email)
        usuario_email = db_session.execute(usuario_sql).scalar_one_or_none()

        if usuario_email:
            flash('E-mail já cadastrado','error')
            return redirect(url_for('registro'))
        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email
            )
            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash('Usuario criado com sucesso', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            print(f'SQLAlchemyError:{e}')
            flash(f'Erro no banco')
            return redirect(url_for('registro'))
        except Exception as e:
            print(f'Erro ao registrar: {e}')
            flash(f'Erro ao registrar','error')
            return redirect(url_for('registro'))
    return render_template("login.html")

@app.route("/")
@login_required
def dashboard():
    # Buscar todos os times no banco
    times = tabela_time.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas
    )


@app.route("/jogadores")
@login_required
def listar_jogadores():
    # Buscar todos os jogadores no banco
    jogadores = tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    # Quando clicar no botão cadastrar
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome").strip()
        numero_camisa = request.form.get("camisanumero") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # 2 - Verificar se foi digitado
        if not nome:
            flash("Preencha o nome", "error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("Preencha o número da camisa", "error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("Preencha a posição", "error")
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash("Preencha o time", "error")
            return redirect(url_for("novo_jogador"))

        # 3 - Salvar no banco
        tabela_jogador.salvar(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    # Select times para escolher no formulario
    #   Buscar todos os times no banco
    times = tabela_time.select_todos()

    #   Buscar todos os jogadores no banco
    jogadores = tabela_jogador.select_todos()

    # Carregar o formulario
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/<id_jogador>", methods=["GET", "POST"])
def editar_jogador(id_jogador):
    # Buscar o jogador no banco
    jogador = tabela_jogador.select_um(id_jogador)

    # Salvar as alterações
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome").strip()
        numero_camisa = request.form.get("camisanumero") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # 2 - Verificar se foi digitado
        if not nome:
            flash("Preencha o nome", "error")
        elif not numero_camisa:
            flash("Preencha o número da camisa", "error")
        elif not posicao:
            flash("Preencha a posição", "error")
        elif not time_id:
            flash("Preencha o time", "error")
        else:
            jogador.nome = nome
            jogador.numero_camisa = numero_camisa
            jogador.posicao = posicao
            jogador.time_id = int(time_id)
            db_session.commit()

            flash("Jogador alterado com sucesso", "success")

        return redirect(url_for("listar_jogadores"))

    # Carregar as informações
    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()
    return render_template("jogadores.html", jogadores=jogadores, editar=jogador, times=times)

@app.route("/times")
def listar_times():
    # Buscar todos os times no banco
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1 - Pegar os valores digitados no form
        nome = request.form.get("nome")
        turma = request.form.get("turma")
        responsavel = request.form.get("responsavel")
        jogadores_ids = request.form.getlist("jogadores")

        # 2 - Verificar se foi digitado
        if not nome:
            flash("Preencha o nome", "error")
            return redirect(url_for("novo_time"))
        if not turma:
            flash("Preencha a turma", "error")
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash("Preencha o responsável", "error")
            return redirect(url_for("novo_time"))

        # 3 - Salvar no banco
        time = tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

        if jogadores_ids:
            for jogador_id in jogadores_ids:
                jogador = tabela_jogador.select_um(jogador_id)
                jogador.time_id = time.id
                db_session.add(jogador)
                db_session.commit()


    times = tabela_time.select_todos()
    jogadores = tabela_jogador.select_todos()
    return render_template("times.html", times=times, jogadores=jogadores)


@app.route("/time/<id_time>")
def detalhes_time(id_time):
    time = tabela_time.select_um(int(id_time))
    jogadores = tabela_jogador.select_por_time(int(id_time))
    partidas = tabela_partida.select_por_time(int(id_time))
    return render_template(
        "time_detalhes.html",
        time=time,
        jogadores=jogadores,
        qtd_jogadores=len(jogadores),
        partidas=partidas,
        qtd_partidas=len(partidas)
    )


@app.route("/times/<int:time_id>")
def detalhes_timee(time_id):
    time_obj = tabela_time.select_um(time_id)
    partidas = tabela_partida.select_partidas_time(time_id)
    jogadores = tabela_jogador.select_jogadores_por_time(time_id)
    estatisticas = tabela_partida.select_estatisticas(time_id)


    return render_template(
        "time_detalhes.html",
        time=time_obj,
        jogadores=jogadores,
        qtd_jogadores=len(jogadores),
        qtd_partidas=len(partidas),
        partidas=partidas,
        estatisticas=estatisticas
    )

@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        # 1 - pegar os campos do formulario
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # 2 - Verificar se foi digitado
        if not time_casa_id:
            flash("Preencha o time_casa", "error")
            return redirect(url_for("nova_partida"))
        if not time_visitante_id:
            flash("Preencha o time_visitante_id", "error")
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash("Preencha o gols_casa", "error")
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash("Preencha o gols_visitante", "error")
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash("Preencha o data_partida", "error")
            return redirect(url_for("nova_partida"))

        # 3 - Verificar se os times são iguais
        if time_casa_id == time_visitante_id:
            flash("Selecione times diferentes ", "error")
            return render_template("partidas.html")

        # 4 - Salvar no banco
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)

@app.route("/movimentacao/nova/<int:id_jogador>")
@app.route("/movimentacao/nova", methods=["GET", "POST"])
@roles_required('admin')
def nova_movimentacao(id_jogador=None):
    if request.method == "POST":
        # 1 - Pegar informaçõe do formulario
        jogador_id = request.form.get("jogador_id")
        time_destino_id = request.form.get("time_destino_id")

        # 2 - Verificar informações selecionadas
        if not jogador_id:
            flash("Selecione o jogador", "error")
            return redirect(url_for("nova_movimentacao"))
        if not time_destino_id:
            flash("Selecione o time de destino", "error")
            return redirect(url_for("nova_movimentacao"))

        # 3 - Salvar no banco
        tabela_movimentacao.salvar(jogador_id,time_destino_id)
        return redirect(url_for("nova_movimentacao"))
    # Carregar dados para movimentação
    movimentacoes = tabela_movimentacao.select_todos()
    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()
    print("dss",id_jogador)

    return render_template(
        "movimentacoes.html",
        movimentacoes=movimentacoes,
        jogadores=jogadores,
        times=times,
        jogador_selecionado_id=id_jogador
    )


if __name__ == "__main__":
    app.run(debug=True, port=5004)
