from flask import Flask, render_template, request, redirect, url_for, flash, g
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        total_jogadores=0,
        total_times=0,
        total_partidas=0,
        proximas_partidas=0,
        times_ranking=0,
    )


@app.route("/jogadores")
def listar_jogadores():
    return render_template("jogadores.html", jogadores=[], editar=None, times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        idade = request.form.get("idade") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

    return render_template("jogadores.html", jogadores=[], editar=None, times=[])


@app.route("/times")
def listar_times():
    return render_template("times.html", times=[], editar=None)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cor = request.form.get("cor", "").strip()

    return render_template("times.html", times=[], editar=None)


@app.route("/partidas")
def listar_partidas():

    return render_template("partidas.html", partidas=[], editar=None, times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        placar_casa = request.form.get("placar_casa") or 0
        placar_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        local = request.form.get("local", "").strip()

    return render_template("partidas.html", partidas=[], editar=None, times=[])


if __name__ == "__main__":
    app.run(debug=True)
