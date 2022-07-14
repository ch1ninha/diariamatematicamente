# gerador de campeonato
@app.route("/start_gerador_campeonato")
def start_gen_camp():
    next_page = request.args.get("next_page")
    return render_template("campeonato/gerador_campeonato.html",
                            next_page=next_page)


@app.route("/home_gerador_campeonato")
def home_gerador_campeonato():
    name_campeonato = session['name_campeonato']
    n_players_campeonato = session['n_players_camp']
    return render_template("campeonato/home_gerador_campeonato.html",
                            name_camp=name_campeonato.capitalize(),
                            n_players_camp=n_players_campeonato,
                            next_page=session['_pagina_calendario'])


@app.route("/autenticar_campeonato", methods=["POST",])
def autenticar_campeonato():
    session['name_campeonato'] = request.form['name_camp']
    session['n_players_camp'] = request.form['n_players_camp']

    # ATENCAO!! CUIDADO!! GAMBIARRA HAHAHS
    session['_pagina_calendario'] = "calendario_campeonato"
    next_page = request.form["next_page"]
    return redirect(next_page)

@app.route("/autenticar_times", methods=["POST",])
def autenticar_times():
    if session['n_players_camp']:
        n_times = int(session['n_players_camp'])
        # Criando um dicionario para salvar os times na sessão
        session['nome_times'] = {}

        for num_time in range(n_times):
            nome_jogador_atual = request.form[f'nome_{num_time}']
            nome_time_atual = request.form[f'time_{num_time}']
            session['nome_times'][f'jogador_{num_time}'] = {
                "nome_jogador": nome_jogador_atual,
                "nome_time": nome_time_atual
            }
    next_page = session['_pagina_calendario'].replace(".html","")
    return redirect(next_page)


@app.route("/calendario_campeonato")
def calendario_campeonato():
    old_team_list = random.shuffle([_x for _x in session['nome_times']])
    # new_team_list = random.shuffle(old_team_list)
    # for n_team in range(len(old_team_list)):
    #    team = random.choice(old_team_list)
    #    new_team_list.append(team)
    #    old_team_list.pop(team)

    return render_template("campeonato/calendario_campeonato.html",
                            lista_times=old_team_list,dic_times=session['nome_times'])
