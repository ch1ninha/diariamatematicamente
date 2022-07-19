from email.policy import default
from logging import warning
from tkinter import N

from pandas import read_sql_query
from flask import Flask, render_template, request, redirect, session, flash, url_for
from Game import Game


from flask_sqlalchemy import SQLAlchemy

arquivo_txt_secrets = open("C:/Users/lucas/Desktop/chininhaNortao/Game/webapp/secrets.txt","r")
secrets_key, password_mysql_local = arquivo_txt_secrets.read().split("\n")

app = Flask(__name__)
app.secret_key = secrets_key

db = SQLAlchemy(app)

uri_sqlalchemy = f'mysql+mysqlconnector://root:{password_mysql_local}@127.0.0.1/matemaniac'
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
    lista_jogadores = list(db_user.query.order_by(db_user.score))[:11]

    usuario_online = session.get("online_user")
    if usuario_online == None:
        return render_template("home.html",jogadores=lista_jogadores,
                               titulo=titulo_site,usuario_online=None)
    return render_template("home.html",jogadores=lista_jogadores,
                           titulo=titulo_site,usuario_online=usuario_online)


@app.route("/new_user")
def new_user():
    if session.get("online_user") != None:
        flash(f"Tem certeza? Você já está logado com o usuario {session['online_user']}","warning")
        # "/login?next_page=new_player")
        # return render_template("new_user.html", titulo="Registrar")
    return render_template("new_user.html", titulo="Registrar")


@app.route("/create", methods=['POST', ])
def create():
    # fazer esse create, ser um registrador de usuarios
    id_nickname = request.form['id_nickname']
    password = request.form['password']

    usuario_create = db_user.query.filter_by(id_nickname=id_nickname).first()

    if usuario_create:
        flash("Já existe um usuario com esse nick. Tente fazer o login.","danger")
        return redirect(url_for("login"))

    novo_usuario = db_user(id_nickname=id_nickname,password=password)
    db.session.add(novo_usuario)
    db.session.commit()
    flash(f"Tudo certo na criação da conta, {id_nickname}", "success")
    return render_template("login.html", next_page="math_game") # precisa do parametro 'next_page'


@app.route("/login")
def login():
    if session.get("online_user") != None:
        flash(f"Você está logado com o usuario: {session['online_user']}", "warning")
        return redirect(url_for("index"))
    next_page = request.args.get("next_page")
    if next_page == None:
        next_page = "math_game"
    return render_template("login.html", next_page=next_page, title="Login")


@app.route("/autenticar", methods=['POST',])
def autenticar():
    user = db_user.query.filter_by(id_nickname=request.form['usuario']).first()
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
            flash("Senha errada! :<", "danger")
            return redirect(url_for('login', next_page='math_game'))
    else:
        flash("Login não efetuado, usuario não encontrado! :(", "danger")
        return redirect(url_for('login', next_page='math_game'))


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
        game = Game()
        dicionario_jogos = game.definir_jogos()
        return render_template("math_game.html",
                               dicionario_jogos=dicionario_jogos)
    else:
        flash("Faça o login para acessar essa página.", "warning")
        return redirect(url_for("index"))

@app.route("/confirmar_respostas", methods=['POST',])
def confirmar_respostas():
    resultados_lista = []
    num_1_lista = []
    num_2_lista = []
    for i in range(10):
        num_1_lista.append(request.form.get(f'jogo_{i}_num_1'))
        num_2_lista.append(request.form.get(f'jogo_{i}_num_2'))
        resultados_lista.append(request.form.get(f'tentativa_{i}'))

    num1_lista = list(map(lambda x: int(x), num_1_lista))
    num2_lista = list(map(lambda x: int(x), num_2_lista))
    lista_numeros = [_ for _ in zip(num1_lista,num2_lista)]
    resultados_lista = list(map(lambda x: int(x), resultados_lista))
    print(lista_numeros)
    for tent in range(len(lista_numeros)):
        jogo_atual = lista_numeros[tent]
        resultado = jogo_atual[0] * jogo_atual[1]
        if resultado == resultados_lista[tent]:
            print(f"ACERTOU: tent {resultado} x {resultados_lista[tent]} res")
        else:
            print(f"ERROU: tent {resultado} x {resultados_lista[tent]} res")
    return redirect(url_for('math_game'))
    # criar pagina de resultado, amanha

    # criar banco de dados para resultados e deixar lá
app.run(debug=True)