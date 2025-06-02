from flask import Flask, render_template, abort, request, redirect, url_for, flash
from flask_mail import Mail
from werkzeug.utils import secure_filename
import sqlite3
from forms import UserForm

conn = sqlite3.connect('flask2.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, surname TEXT, age INTEGER, gender TEXT, file TEXT)')
conn.close()


app = Flask(__name__)
mail = Mail(app)

from dataclasses import dataclass


app.secret_key = "supersecret"

@dataclass
class User:
    username: str
    surname: str
    age: int
    gender: str

    def __str__(self):
        return f"User(username={self.username}, surname={self.surname}, age={self.age}"
    

users_all = [
    User("Ali", "Khan", 32, "erkek"),
    User("Ayşe", "Yılmaz", 28, "kız"),
    User("Mehmet", "Demir", 45, "erkek"),
    User("Fatma", "Çelik", 30, "kız"),
]


@app.route('/')
def hello_world():
    #abort(404)
    return render_template('home.html')

@app.route('/index')
def index():

    return render_template('flask2.html', datas = {
        'users' : users_all,
    })

@app.route("/uploader", methods=["POST"])
def upload_file():

    try:
        file = request.files['file']
        file.save('static/uploads/' + file.filename)
    except Exception as e:
        flash("File upload failed: " + str(e), "error")
        return redirect(url_for('index'))
    
    flash("File upload successful", "success")
    return redirect(url_for('index'))


@app.route('/user/list', methods=['GET', 'POST'])
def user_list():

    conn = sqlite3.connect('flask2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = list(cursor.fetchall())
    conn.close()
    return render_template('user_list.html', users=users, form = UserForm())


@app.route('/user/add', methods=['POST'])
def user_add():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form.get('username')
            surname = request.form.get('surname')
            age = request.form.get('age')
            gender = request.form.get('gender')
            
            if form.file.data:
                file = form.file.data
                filename = secure_filename(file.filename)
                file.save('static/uploads/'+filename)


            conn = sqlite3.connect('flask2.db')
            cursor = conn.cursor()
            cursor.execute(''' INSERT INTO users (username, surname, age, gender, file)
                            VALUES (?, ?, ?, ?, ?)''', (username, surname, age, gender, filename))
            conn.commit()
            conn.close()
            flash("File upload successful", "success")

        else:
            flash("Form validation failed", "error")
            return redirect(url_for('user_list', form=form))
        
        flash("that is about GET", "error")
        return redirect(url_for('user_list', form=form))

if __name__ == '__main__':
    app.run(port=5000, debug=True)