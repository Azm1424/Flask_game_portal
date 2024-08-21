import sqlite3


def create_table():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS games(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    img TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    rating_igdb REAL NOT NULL,
                    trailer TEXT NOT NULL,
                    platforms TEXT NOT NULL,
                    avg_users_rating REAL NOT NULL
                    )''')
    conn.commit()
    conn.close()

def create_user_table():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                        )''')
    conn.commit()
    conn.close()

def create_profiles_table():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS profiles(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            name TEXT,
                            age TEXT,
                            country TEXT,
                            city TEXT,
                            contacts TEXT,
                            favourite_game TEXT
                            )''')
    conn.commit()
    conn.close()

def create_reviews_table():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            game_id INTEGER NOT NULL,
                            username TEXT NOT NULL,
                            review TEXT NOT NULL,
                            rating INTEGER NOT NULL,
                            created DATE DEFAULT (date('now','localtime'))
                            )''')
    conn.commit()
    conn.close()

def add_game(img, name, description, genre, rating_igdb, trailer, platforms, avg_users_rating):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO games(img, name, description, genre, rating_igdb, trailer, platforms, avg_users_rating)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (img, name, description, genre, rating_igdb, trailer, platforms, avg_users_rating))
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users(username, email, password)
                    VALUES(?, ?, ?)''', (username, email, password))
    conn.commit()
    conn.close()

def add_profile(username):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO profiles(username) VALUES(?)''', (username,))
    conn.commit()
    conn.close()

def add_review(game_id, username, review, rating):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO reviews(game_id, username, review, rating)
                        VALUES(?, ?, ?, ?)''', (game_id, username, review, rating))
    conn.commit()
    conn.close()

def get_games():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    games = cursor.execute('''SELECT * FROM games''').fetchall()
    conn.close()
    return games

def get_users():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    users = cursor.execute('''SELECT * FROM users''').fetchall()
    conn.close()
    return users

def get_reviews(game_id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    reviews = cursor.execute('''SELECT * FROM reviews WHERE game_id=?''', (game_id,)).fetchall()
    conn.close()
    return reviews

def get_usernames_reviews(username):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    reviews = cursor.execute('''SELECT * FROM reviews WHERE username=?''', (username,)).fetchall()
    conn.close()
    return reviews

def get_game_by_id(id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    game = cursor.execute('''SELECT id, name FROM games WHERE id=?''', (id,)).fetchone()
    conn.close()
    return game

def get_users_ratings():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    ratings = cursor.execute('''SELECT id, name, avg_users_rating FROM games ORDER BY avg_users_rating DESC LIMIT 10''').fetchall()
    conn.close()
    return ratings

def get_experts_ratings():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    ratings = cursor.execute('''SELECT id, name, rating_igdb FROM games ORDER BY rating_igdb DESC LIMIT 10''').fetchall()
    conn.close()
    return ratings

def get_profile_data(username):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    profile = cursor.execute('''SELECT * FROM profiles WHERE username=?''', (username,)).fetchone()
    conn.close()
    return profile

def check_review(game_id, username):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    check_review = cursor.execute('''SELECT * FROM reviews WHERE game_id=? AND username=?''', (game_id, username)).fetchone()
    conn.close()
    return bool(check_review)

def update_review(review, rating, game_id, username):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE reviews SET review=?, rating=?, created=date('now','localtime') WHERE game_id=? AND username=?''', (review, rating, game_id, username))
    conn.commit()
    conn.close()

def update_profile(name, age, country, city, contacts, favourite_game, username):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE profiles SET name=?, age=?, country=?, city=?, contacts=?, favourite_game=? WHERE username=?''',
        (name, age, country, city, contacts, favourite_game, username))
    conn.commit()
    conn.close()

def del_user(id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM users WHERE id=?''', (id,))
    conn.commit()
    conn.close()


def del_game(id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM games WHERE id=?''', (id,))
    conn.commit()
    conn.close()

def drop_table():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE profiles''' )
    conn.commit()
    conn.close()

def add_column():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute('''ALTER TABLE games ADD avg_users_rating REAL''' )
    conn.commit()
    conn.close()

def update_column():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE games SET platforms=? WHERE id=?''', ('PC, PlayStation 4/5, Xbox', 3))
    conn.commit()
    conn.close()

def update_avg_users_rating(avg_users_rating, id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(
        '''UPDATE games SET avg_users_rating=? WHERE id=?''', (avg_users_rating, id))
    conn.commit()
    conn.close()

# add_profile('fdggderg')
# update_column()
# add_column()
# drop_table()
# create_table()
# create_user_table()
# create_reviews_table()
# create_profiles_table()

# add_game('https://image.api.playstation.com/vulcan/ap/rnd/202302/2321/3098481c9164bb5f33069b37e49fba1a572ea3b89971ee7b.jpg', '''Baldur's Gate III''',
#          '''Baldur's Gate III — ізометрична рольова відеогра, розроблена Larian Studios. Це третя основна гра в серії Baldur's Gate, заснована на настільній рольовій системі Dungeons & Dragons 5-го видання.''',
#          'Рольова відеогра, Пригодницька відеогра, Стратегічна відеогра', 9.7, 'https://www.youtube.com/embed/XuCfkgaaa08?si=BHxTu1Z3-idQYJxg', 'PC, PlayStation 5, Xbox', 0)
#
# add_game('https://image.api.playstation.com/vulcan/img/rnd/202010/2217/LsaRVLF2IU2L1FNtu9d3MKLq.jpg', '''God of War''',
#          '''God of War — медіафраншиза, зосереджена навколо однойменної серії відеоігор жанрів Hack and slash і Action-adventure, створених за мотивами давньогрецької міфології. Головним героєм усіх ігор серії є Кратос — спартанський генерал, який кидає виклик богам.''',
#          'Пригодницький бойовик, Файтинг, Рольова відеогра, Adventure', 9.4, 'https://www.youtube.com/embed/K0u_kAWLJOA?si=xhbuYwyKzjZ4j1ZJ', 'PC, PlayStation 4/5', 0)
#
# add_game('https://content1.rozetka.com.ua/goods/images/big/364854365.jpg',
#          '''Divinity: Original Sin II''',
#          '''Divinity: Original Sin II — це шоста гра в серії Divinity та непряме продовження Divinity: Original Sin: ізометрична одно- та багатокористувацька фентезійна рольова гра з тактичними покроковими боями. Центральна тема гри: «ваше походження впливає на те, ким ви є і які шанси ви отримуєте в житті».''',
#          'Рольова відеогра, Пригодницька відеогра, Стратегічна відеогра',
#          9.5,
#          'https://www.youtube.com/embed/bTWTFX8qzPI?si=xEKCFlQ0e39X4fFh',
#          'PC, PlayStation 4/5, Xbox',
#          0
#          )

# add_game('https://gaming-cdn.com/images/products/2198/616x353/hollow-knight-pc-mac-game-steam-cover.jpg?v=1705490619',
#          '''Hollow Knight''',
#          '''Hollow Knight — це мультиплатформна відеогра в жанрі метроїдванія,
#          випущена інді-студією Team Cherry у 2017 році для ПК. Спочатку гра вийшла на Windows, але місяцем пізніше
#          була портована розробниками на Linux і macOS. Розробка гри була спонсорована через сервіс Kickstarter.
#          Гра розповідає про пригоди та відкриття безіменного жука, якого усі називають просто Лицарем, у давно
#          покинутому королівстві комах Святогнізді (Hallownest). Деякі критики назвали гру однією з найбільш
#          атмосферних і якісних метроїдваній, а також класикою жанру.''',
#          'Метроїдванія',
#          8.7,
#          'https://www.youtube.com/embed/UAO2urG23S4?si=JmxziwUR618RRYo3',
#          'PC, PlayStation 4, Xbox, Nintendo Switch',
#          0
#          )

# add_game('https://cloudgaminghub.net.ua/wp-content/uploads/2024/04/counter-strike-2-update-1024x576.webp',
#          '''Counter-Strike 2''',
#          '''Counter-Strike 2 (скорочено CS 2) — багатокористувацька гра в жанрі тактичного шутера від першої
#          особи, розроблена компанією Valve. Є 5-ю грою в серії Counter-Strike. Valve анонсувала гру 22 березня 2023
#          року, оголосивши, що вона вийде влітку 2023 року. Компанія почала розсилати перші запрошення на обмежений
#          тест для Counter-Strike 2 в ніч з 22 на 23 березня 2023 року, доступний тільки для користувачів Windows,
#          доступ до нової версії гри отримали не всі гравці, а лише частина. За офіційною інформацією, компанія
#          спиралася на кількість годин на офіційних серверах і на Trust Factor. Реліз гри відбувся 27 вересня 2023 року.
#          Counter Strike 2 замінила CS:GO, яка була видалена зі Steam.''',
#          'Шутер від першої особи',
#          8.0,
#          'https://www.youtube.com/embed/nSE38xjMLqE?si=Q1ycZ59xftdtYORC',
#          'PC',
#          0
#          )