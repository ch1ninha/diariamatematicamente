from random import randint

class Game:
    random = __import__("random")
    def __init__(self) -> None:
        self.numeros_game = [randint(1,19) for _ in range(20)]

    def definir_jogos(self):
        jogos = {}
        for n_game in range(10):
            jogos[n_game] = {"num_1":self.numeros_game.pop(),
                             "num_2":self.numeros_game.pop()}
        return jogos

game = Game()