from flask import Flask, render_template, request

app = Flask(__name__)


lista_jogadores = ['inter673','inter657','snow']


@app.route("/")
def index():
    return render_template("home.html",jogadores=lista_jogadores)

@app.route("/new_player")
def new_player():
    return render_template("new_player.html")

@app.route("/create",methods=['POST',])
def create():
    nick_player = request.form['nick_player']
    lista_jogadores.append(nick_player)
    return render_template("home.html",jogadores=lista_jogadores)


app.run(debug=True)