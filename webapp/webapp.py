from flask import Flask, render_template, request, redirect, session, flash, url_for
from Jogador import Player
from usuario import Usuario

from dao import PlayerDao, UsuarioDao
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "chininha"
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "C3!T4do1Do"
app.config['MYSQL_DB'] = "matemaniac"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)
player_dao = PlayerDao(db)
user_dao = UsuarioDao(db)

@app.route("/")
def index():
    lista_jogadores = player_dao.listar()
    return render_template("home.html",jogadores=lista_jogadores,titulo="titulo")

@app.route("/new_player")
def new_player():
    if 'online_user' not in session or session['online_user'] == None:
        return redirect(url_for("login", next_page=url_for("new_player"))) # "/login?next_page=new_player")
    return render_template("new_player.html",titulo="titulo")

@app.route("/create",methods=['POST',])
def create():
    nick_player = request.form['nick_player']
    player = Player("vazio",nick_player)
    player_dao.salvar(player)
    return redirect(url_for("index"))

@app.route("/login")
def login():
    if session['online_user'] != None:
        flash("Você JA está logado...", "warning")
        return redirect(url_for("index"))
    next_page = request.args.get("next_page")
    return render_template("login.html",next_page=next_page)

@app.route("/autenticar", methods=['POST',])
def autenticar():
    user = user_dao.buscar_por_id(request.form['usuario'])

    if session['online_user'] != None:
        flash("Você já está logado manoo!","warning")
        return redirect(url_for("index"))

    if user:
        if request.form['password'] == user.password:
            session['online_user'] = user.nickname
            flash(f"Login efetuado com sucesso! Bem-vindo, {user.nickname}", "success")
            next_page = request.form['next_page']
            return redirect(next_page)
        else:
            flash("Senha errada! :<","error")
            return redirect(url_for("login"))
    else:
        flash("Login não efetuado, usuario não encontrado! :(", "error")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if session['online_user'] == None:
        flash("Você não está logado...", "warning")
        return redirect(url_for("index"))
    flash(f"{session['online_user']}, deslogado com sucesso!", "success")
    session['online_user'] = None
    return redirect(url_for("index"))

@app.route("/math_game")
def math_game():
    if session['online_user'] != None:
        return render_template("math_game.html")
    else:
        flash("Você não está logado...", "warning")
        return redirect(url_for("index"))


# gerador de campeonato
@app.route("/start_gerador_campeonato")
def start_gen_camp():
    next_page = request.args.get("next_page")
    return render_template("campeonato/gerador_campeonato.html",next_page=next_page)

@app.route("/home_gerador_campeonato")
def home_gerador_campeonato():

    return render_template("campeonato/home_gerador_campeonato.html",
                            name_camp=name_campeonato,
                            n_players_camp=n_players_campeonato)

@app.route("/autenticar_campeonato",methods=["POST",])
def autenticar_campeonato():
    global name_campeonato, n_players_campeonato

    name_campeonato = request.form['name_camp']
    n_players_campeonato = request.form['n_players_camp']
    
    next_page = request.form["next_page"]
    return redirect(next_page)


app.run(debug=True)