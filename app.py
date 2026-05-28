from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import init_db, get_db
from werkzeug.security import  generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'abdu1234'

init_db()


#auth_routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = generate_password_hash(password)

        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
            db.commit()
            return redirect(url_for('login'))
        except:
            flash('Username already taken.')
            return redirect(url_for('register'))
        finally:
            db.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('inventory'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))



@app.route('/inventory')
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    parts = db.execute(
        'SELECT * FROM parts WHERE user_id = ? ORDER BY name ASC',
        (session['user_id'],)
    ).fetchall()
    db.close()

    return render_template('inventory.html', parts=parts, username=session['username'])


if __name__ == '__main__':
    app.run(debug=True)