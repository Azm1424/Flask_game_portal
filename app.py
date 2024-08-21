from flask import Flask, render_template, request, redirect, session, url_for
from database import *
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, EmailField, PasswordField, TextAreaField, validators
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = '$#*V$*#(YM*$#Y664$C(M(*$CY(*#Idfodfjs3242342'

class RegistrationForm(FlaskForm):
    username = StringField('Введіть свій нікнейм:', validators=[validators.InputRequired(), validators.DataRequired(), validators.Length(max=20)])
    email = EmailField('Введіть пошту:', validators=[validators.InputRequired(), validators.DataRequired()])
    password = PasswordField('Введіть пароль:', validators=[validators.InputRequired(), validators.DataRequired(), validators.Length(min=8, max=15)])
    submit_reg = SubmitField('Зареєструватись')
    submit_login = SubmitField('Увійти')

class ProfileForm(FlaskForm):
    name = StringField("Ваше ім'я:", validators=[validators.Length(max=20)])
    age = StringField("Ваш вік:", validators=[validators.Length(max=3)])
    country = StringField("Ваша країна:", validators=[validators.Length(max=30)])
    city = StringField("Ваше місто:", validators=[validators.Length(max=30)])
    contacts = StringField("Ваші контактні дані:", validators=[validators.Length(max=100)])
    favourite_game = StringField("Ваша улюблена гра:", validators=[validators.Length(max=40)])
    submit = SubmitField('Підтвердити')

class ReviewForm(FlaskForm):
    review = TextAreaField('Напишіть огляд: ', validators=[validators.DataRequired(), validators.Length(max=2000)])
    rating = SelectField('Поставте оцінку: ', validators=[validators.DataRequired()])
    submit = SubmitField('Відправити')

@app.route('/')
def index():
    games = get_games()
    return render_template('index.html', games=games)

@app.route('/<int:id>/', methods=['GET', 'POST'])
def inspection_of_the_game(id):
    reviews = get_reviews(id)
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    game = cursor.execute('''SELECT * FROM games WHERE id=?''', (id,)).fetchone()
    conn.commit()
    conn.close()
    form = ReviewForm()
    form.rating.choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]
    if request.method == 'POST':
        checked_review = check_review(id, session['username'])
        if not checked_review:
            avg_users_rating = 0
            for i in reviews:
                avg_users_rating += i[4]
            avg_users_rating = round((avg_users_rating + int(request.form['rating'])) / (len(reviews) + 1), 1)
            update_avg_users_rating(avg_users_rating, id)
            add_review(id, session['username'], request.form['review'], request.form['rating'])
            return redirect(url_for('inspection_of_the_game', id=id))
        else:
            avg_users_rating = 0
            for i in reviews:
                if i[2] != session['username']:
                    avg_users_rating += i[4]
            avg_users_rating = round((avg_users_rating + int(request.form['rating'])) / (len(reviews)), 1)
            update_avg_users_rating(avg_users_rating, id)
            update_review(request.form['review'], request.form['rating'], id, session['username'])
            return redirect(url_for('inspection_of_the_game', id=id))

    return render_template('game.html', game=game, form=form, reviews=reviews)

@app.route('/reg/', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if request.method == 'POST':
        users = get_users()
        for i in users:
            if request.form['username'] == i[1]:
                error_mess = f'⚠️ Користувач з іменем {i[1]} вже існує'
                return render_template('reg_error.html', error_mess=error_mess)
            if request.form['email'] == i[2]:
                error_mess = f'⚠️ Пошта {i[2]} вже зареєстрована'
                return render_template('reg_error.html', error_mess=error_mess)
        add_user(request.form['username'], request.form['email'], generate_password_hash(request.form['password']))
        add_profile(request.form['username'])
        session['username'] = request.form['username']
        return redirect('/')
    return render_template('registration.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if request.method == 'POST':
        users = get_users()
        for i in users:
            if request.form['email'] == i[2] and check_password_hash(i[3], request.form['password']):
                session['username'] = i[1]
                return redirect('/')
        user_not_found = '⚠️ Користувача не знайдено. Перевірте введені дані'
        return render_template('login.html', form=form, user_not_found=user_not_found)
    return render_template('login.html', form=form)

@app.route('/<username>/', methods=['GET', 'POST'])
def profile(username):
    profile = get_profile_data(username)
    reviews = get_usernames_reviews(username)
    games = []
    for i in reviews:
        games.append(get_game_by_id(i[1]))
    form = ProfileForm()
    if request.method == 'POST':
        update_profile(request.form['name'], request.form['age'], request.form['country'], request.form['city'], request.form['contacts'], request.form['favourite_game'], session['username'])
        return redirect(url_for('profile', username=username))
    return render_template('profile.html', form=form, profile=profile, reviews=reviews, games=games)

@app.route('/logout/')
def end_session():
    session.pop('username', None)
    return redirect('/')

@app.route('/search_results/', methods=['GET', 'POST'])
def search_results():
    games = get_games()
    list_of_searched_games = []
    if request.method == 'POST':
        for i in games:
            if request.form['search'].lower() in i[2].lower():
                list_of_searched_games.append(i)
    return render_template('searched.html', searched=list_of_searched_games)

@app.route('/top_10_users/')
def top_10_users():
    ratings = get_users_ratings()
    ratings_lists = []
    count = 0
    for i in ratings:
        count += 1
        i = list(i)
        i.insert(0, count)
        ratings_lists.append(i)
    return render_template('top_10.html', ratings=ratings_lists)

@app.route('/top_10_experts/')
def top_10_experts():
    ratings = get_experts_ratings()
    ratings_lists = []
    count = 0
    for i in ratings:
        count += 1
        i = list(i)
        i.insert(0, count)
        ratings_lists.append(i)
    return render_template('top_10.html', ratings=ratings_lists)

if __name__ == '__main__':
    app.run(debug=True)