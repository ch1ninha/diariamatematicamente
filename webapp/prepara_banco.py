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
    CREATE TABLE `db_user` (
      `id_nickname` varchar(50) COLLATE utf8_bin NOT NULL,
      `password` varchar(20) COLLATE utf8_bin NOT NULL,
      `score` INT COLLATE utf8_bin NOT NULL DEFAULT 0,
      PRIMARY KEY (`id_nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO matemaniac.db_user (id_nickname, password) VALUES (%s, %s)',
      [
            ('luan', 'flask'),
            ('nico', '7a1'),
            ('danilo', 'vegas'),
            ('chininha', '123')
      ])

cursor.execute('select * from matemaniac.db_user')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[0])

# commitando senão nada tem efeito
conn.commit()
cursor.close()