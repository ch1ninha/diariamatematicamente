from Jogador import Player
from usuario import Usuario

SQL_DELETE_PLAYER = 'delete from player where id = %s'
SQL_PLAYER_POR_ID = 'SELECT id, name, nickname, score from player where id = %s'
SQL_USER_POR_ID = 'SELECT id_nickname, name, password from user where id_nickname = %s'
SQL_UPDATE_PLAYER = 'UPDATE player SET name=%s, nickname=%s, score=%s where id = %s'
SQL_SEARCH_PLAYERS = 'SELECT id, name, nickname, score from matemaniac.player'
SQL_CREATE_PLAYER = 'INSERT into player (name, nickname, score) values (%s, %s, %s)'


class PlayerDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, player):
        cursor = self.__db.connection.cursor()

        if (player.id):
            cursor.execute(SQL_UPDATE_PLAYER, (player.name, player.nickname, player.score, player.id))
        else:
            cursor.execute(SQL_CREATE_PLAYER, (player.name, player.nickname, player.score))
            player.id = cursor.lastrowid
        self.__db.connection.commit()
        return player

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SEARCH_PLAYERS)
        players = traduz_players(cursor.fetchall())
        return players

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PLAYER_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Player(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETE_PLAYER, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USER_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_players(players):
    def cria_player_com_tupla(tupla):
        return Player(tupla[1], tupla[2], id=tupla[0])
    return list(map(cria_player_com_tupla, players))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])