from flask import Flask, render_template, request, redirect, session, flash, url_for
from Jogador import Player
from usuario import Usuario

app = Flask(__name__)
app.secret_key = "chininha"

# Jogadores para colocar na lista inicial
p1 = Player("inter673")
p2 = Player("inter657")
p3 = Player("snow")

# Usuarios para termos acessos ao site
user1 = Usuario("lucas","chininha","123")
user2 = Usuario("aguero","o_brabo_arg","321")
user3 = Usuario("neymar","ney+mar","vasco")

usuarios = {user1.nickname : user1,
            user2.nickname : user2,
            user3.nickname : user3}

lista_jogadores = [p1,p2,p3]

@app.route("/")
def index():
    return render_template("home.html",jogadores=lista_jogadores,titulo="titulo")

@app.route("/new_player")
def new_player():
    if 'online_user' not in session or session['online_user'] == None:
        return redirect(url_for("login", next_page=url_for("new_player"))) # "/login?next_page=new_player")
    return render_template("new_player.html",titulo="titulo")

@app.route("/create",methods=['POST',])
def create():
    nick_player = request.form['nick_player']
    player = Player(nick_player)
    lista_jogadores.append(player)
    return redirect(url_for("index"))

@app.route("/login")
def login():
    next_page = request.args.get("next_page")
    return render_template("login.html",next_page=next_page)

@app.route("/autenticar", methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        user = usuarios[request.form['usuario']]
        if request.form['password'] == user.senha:
            session['online_user'] = user.nickname
            flash(f"Login efetuado com sucesso! Bem-vindo, {user.nickname}")
            next_page = request.form['next_page']
            return redirect(next_page)
    else:
        flash("Login não efetuado... :(")
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    flash(f"{session['online_user']}, deslogado com sucesso!")
    session['online_user'] = None
    return redirect(url_for("index"))
app.run(debug=True)