import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='C3!T4do1Do',
                       host='127.0.0.1', port=3306)


# Descomente se quiser desfazer o banco...
# conn.cursor().execute("DROP DATABASE `matemaniac`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `matemaniac` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `matemaniac`;
    CREATE TABLE `player` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8_bin NOT NULL,
      `nickname` varchar(40) COLLATE utf8_bin NOT NULL,
      `score` int(9) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `user` (
      `id_nickname` varchar(8) COLLATE utf8_bin NOT NULL,
      `name` varchar(20) COLLATE utf8_bin NOT NULL,
      `password` varchar(10) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id_nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO matemaniac.user (id_nickname, name, password) VALUES (%s, %s, %s)',
      [
            ('luan', 'Luan Marques', 'flask'),
            ('nico', 'Nico', '7a1'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('select * from matemaniac.user')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO matemaniac.player (name, nickname, score) VALUES (%s, %s, %s)',
      [
            ('Luan Marques', 'luan', '0'),
            ('Nico', 'nico', '2'),
            ('Danilo', 'danilo', '5')
      ])

cursor.execute('select * from matemaniac.player')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()