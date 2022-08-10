from flask import Flask, render_template, request, redirect, session, flash, url_for

from Game import Game
from datetime import datetime
from Funcoes import db_mapear_numeros

from flask_sqlalchemy import SQLAlchemy

arquivo_txt_secrets = open("C:/Users/lucas/Desktop/chininhaNortao/Matemaniac/webapp/secrets.txt","r")
secrets_key, password_mysql_local = arquivo_txt_secrets.read().split("\n")

app = Flask(__name__)
app.secret_key = secrets_key

db = SQLAlchemy(app)

uri_sqlalchemy = f'mysql+mysqlconnector://root:{password_mysql_local}@127.0.0.1/matemaniac'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_sqlalchemy

# declaração das classes para sqlalchemy
class db_user(db.Model):
    id_nickname = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    score = db.Column(db.INT(), nullable=False,default=0)
    qtde_jogos = db.Column(db.INT(), nullable=False,default=0)
    def __repr__(self):
        return f'id_nickname: {self.id_nickname}'

class db_game(db.Model):
    id_game = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dia_game = db.Column(db.DateTime, default=datetime.now() , nullable=False)
    num_da_tentativa = db.Column(db.Integer, nullable=False)
    num_1 = db.Column(db.Integer, nullable=False)
    num_2 = db.Column(db.Integer, nullable=False)
    acertou = db.Column(db.Boolean, nullable=False)
    id_nickname = db.Column(db.String(50),
                            db.ForeignKey('db_user.id_nickname'),
                            nullable=False)
    def __repr__(self):
        return f'id_game: {self.id_game} | user: {self.id_nickname}'

@app.route("/")
def index():
    usuario_online = session.get("online_user")
    if usuario_online:
        return redirect(url_for("ranking_page"))
    return render_template("home_page.html",usuario_online=usuario_online)

@app.route("/ranking_page")
def ranking_page():
    lista_jogadores = list(db_user.query.order_by(db_user.score.desc()))[:11]

    usuario_online = session.get("online_user")
    if usuario_online:
        return render_template("ranking.html",jogadores=lista_jogadores,
                               usuario_online=usuario_online)
    return redirect(url_for("index"))


@app.route("/new_user")
def new_user():
    if session.get("online_user") != None:
        flash(f"Tem certeza? Você já está logado com o usuario {session['online_user']}","warning")
    return render_template("new_user.html")


@app.route("/create", methods=['POST', ])
def create():
    # fazer esse create, ser um registrador de usuarios
    id_nickname = request.form['id_nickname']
    password = request.form['password']

    usuario_create = db_user.query.filter_by(id_nickname=id_nickname).first()

    if usuario_create:
        flash("Já existe um usuario com esse nome. Tente fazer o login.","danger")
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
    return render_template("login.html", next_page=next_page)


@app.route("/autenticar", methods=['POST',])
def autenticar():
    user = db_user.query.filter_by(id_nickname=request.form['usuario']).first()
    
    if session.get("online_user") != None:
        flash("Você já está logado manoo!", "warning")
        return redirect(url_for("index"))

    if user:
        if request.form['password'] == user.password:
            session['online_user'] = user.id_nickname
            flash(f"Login efetuado com sucesso! Bem-vindo, {user.id_nickname}", "success")
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
                               dicionario_jogos=dicionario_jogos,
                               next_page="result_game")
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
    dicionario_resultado = {'acertou':0,
                            'errou':0,
                            'tentativas':0}
    dicionario_jogos = {}
    tentativas = 0
    for tent in range(len(lista_numeros)):
        jogo_atual = lista_numeros[tent]
        resultado = jogo_atual[0] * jogo_atual[1]
        tentativas += 1
        dicionario_jogos[tent] = {"num1":jogo_atual[0],
                                  "num2":jogo_atual[1],
                                  "tentativa":resultados_lista[tent],
                                  "resultado":resultado}
        
        if resultado == resultados_lista[tent]:
            dicionario_resultado["acertou"] = dicionario_resultado["acertou"] + 1
        else:
            dicionario_resultado["errou"] = dicionario_resultado["errou"] + 1
        dicionario_resultado["tentativas"] = tentativas

    qtde_certa = dicionario_resultado["acertou"]
    qtde_err = dicionario_resultado["errou"]

    session['jogo_resultado'] = (qtde_certa, qtde_err)
    session['dicio_jogo'] = dicionario_jogos

    return redirect(url_for("result_game"))

@app.route("/result_game")
def result_game():
    if session.get("dicio_jogo"):
        qtde_certa, qtde_err = session.get("jogo_resultado")
        flash(f"Você acertou {qtde_certa} e errou {qtde_err} questões.",'success')

        dicionario_jogos = session.get("dicio_jogo")

        usuario_jogo_atual = session.get('online_user')
        user = db_user.query.filter_by(id_nickname=usuario_jogo_atual).first()
        user.score = user.score + qtde_certa
        user.qtde_jogos = user.qtde_jogos + 1
        db.session.commit()

        for _tent, _num1, _num2, _acertou in db_mapear_numeros(dicionario_jogos):
            nova_tent_jogo = db_game(num_da_tentativa=_tent,
                                     num_1=_num1,
                                     num_2=_num2,
                                     acertou=_acertou,
                                     id_nickname=usuario_jogo_atual)
            db.session.add(nova_tent_jogo)
            db.session.commit()

        return render_template("result_game.html", dicio_jogo=dicionario_jogos)
    else:
        flash(f"Não receber seu jogo!","danger")
        return redirect(url_for("math_game"))

app.run(debug=True)