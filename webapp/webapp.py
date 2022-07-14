from email.policy import default
from logging import warning
from flask import Flask, render_template, request, redirect, session, flash, url_for
import random

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "chininha"

db = SQLAlchemy(app)

uri_sqlalchemy = 'mysql+mysqlconnector://root:C3!T4do1Do@127.0.0.1/matemaniac'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_sqlalchemy


# é o Jogos na aula da alura
class db_user(db.Model):
    id_nickname = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    score = db.Column(db.INT(), nullable=False,default=0)
    def __repr__(self):
        return f'id_nickname: {self.id_nickname}'

titulo_site = "Matemaniac"
@app.route("/")
def index():
    lista_jogadores = db_user.query.order_by(db_user.score) # = player_dao.listar()

    return render_template("home.html",jogadores=lista_jogadores,
                            titulo=titulo_site)


@app.route("/new_player")
def new_player():
    if session.get("online_user") == None:
        # "/login?next_page=new_player")
        return redirect(url_for("login", next_page=url_for("new_player")))
    return render_template("new_player.html", titulo=titulo_site)


@app.route("/create", methods=['POST', ])
def create():
    # fazer esse create, ser um registrador de usuarios
    id_nickname = request.form['id_nickname']
    password = request.form['password']

    usuario_create = db_user.query.filter_by(id_nickname=id_nickname).first()

    if usuario_create:
        flash("Já existe um usuario com esse nick. :(","error")
        return redirect(url_for("index"))

    novo_usuario = db_user(id_nickname=id_nickname,password=password)
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login")
def login():
    if session.get("online_user") != None:
        flash("Você JA está logado...", "warning")
        return redirect(url_for("index"))
    next_page = request.args.get("next_page")
    return render_template("login.html", next_page=next_page)


@app.route("/autenticar", methods=['POST',])
def autenticar():
    user = db_user.query.filter_by(id_nickname=request.form['usuario']).first()
    print(f"------- {user} --------")
    if session.get("online_user") != None:
        flash("Você já está logado manoo!", "warning")
        return redirect(url_for("index"))

    if user:
        if request.form['password'] == user.password:
            session['online_user'] = user.id_nickname
            flash(
                f"Login efetuado com sucesso! Bem-vindo, {user.id_nickname}", "success")
            next_page = request.form['next_page']
            return redirect(next_page)
        else:
            flash("Senha errada! :<", "error")
            return redirect(url_for("login"))
    else:
        flash("Login não efetuado, usuario não encontrado! :(", "error")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if session.get("online_user") == None:
        flash("Você não está logado...", "warning")
        return redirect(url_for("index"))
    flash(f"{session['online_user']}, deslogado com sucesso!", "success")
    session['online_user'] = None
    return redirect(url_for("index"))


@app.route("/math_game")
def math_game():
    if session.get("online_user") != None:
        return render_template("math_game.html")
    else:
        flash("Você não está logado...", "warning")
        return redirect(url_for("index"))

app.run(debug=True)