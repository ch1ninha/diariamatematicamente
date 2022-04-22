class Score:
    def __init__(self,game):
        self.game = game
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

    