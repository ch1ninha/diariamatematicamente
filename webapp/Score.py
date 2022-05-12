class Score:
    def __init__(self,obj_game):
        self.obj_game = obj_game
        self._score = 0
        self._correct = 0
        self._error = 0
        self._trying = 0

    # métodos getter's e setter's
    def get_score(self):
        return self._score
    def set_score(self,score):
        self._score = score
    def get_correct(self):
        return self._correct
    def set_correct(self,correct):
        self._correct = correct
    def get_error(self):
        return self._error
    def set_error(self,error):
        self._error = error
    def get_trying(self):
        return self._trying
    def set_trying(self,trying):
        self._trying = trying

    def tentativa(self):
        tentativa = self.get_trying()
        tentativa += 1
        self.set_trying(tentativa)
    
    # métodos essenciais
    def conferir_pontuacao(self):
        _games = self.obj_game.game
        if self.obj_game.status:
            for rep_jogo in _games:
                self.tentativa()
                acertou = self.get_correct()
                errou = self.get_error()
                if _games[rep_jogo]['resposta'] == _games[rep_jogo]['tentativa']:
                    acertou += 1
                    self.set_correct(acertou)
                else:
                    errou += 1
                    self.set_error(errou)
        _confere = {"tentativas":self.get_trying(),
                    "acertou":self.get_correct(),
                    "errou":self.get_error()}
        return _confere

        