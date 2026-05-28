from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import init_db, get_db
from werkzeug.security import  generate_password_hash, check_password_hash
from logic import get_low_stock_parts


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


#inventory

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

    low_stock = get_low_stock_parts(parts)

    return render_template('inventory.html', parts=parts, username=session['username'])

#part Add
@app.route('/add', methods=['GET', 'POST'])
def add_part():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        category = request.form['category']
        threshold = int(request.form['threshold'])

        db = get_db()
        db.execute(
            'INSERT INTO parts (user_id, name, quantity, category, low_stock_threshold) VALUES (?, ?, ?, ?, ?)',
            (session['user_id'], name, quantity, category, threshold)
        )
        db.commit()
        db.close()

        flash('Part added successfully.')
        return redirect(url_for('inventory'))

    return render_template('add.html')


#Part Edit
@app.route('/edit/<int:part_id>', methods=['GET', 'POST'])
def edit_part(part_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    part = db.execute(
        'SELECT * FROM parts WHERE id = ? AND user_id = ?',
        (part_id, session['user_id'])
    ).fetchone()

    if part is None:
        db.close()
        return redirect(url_for('inventory'))

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        category = request.form['category']
        threshold = int(request.form['threshold'])

        db.execute(
            'UPDATE parts SET name = ?, quantity = ?, category = ?, low_stock_threshold = ? WHERE id = ? AND user_id = ?',
            (name, quantity, category, threshold, part_id, session['user_id'])
        )
        db.commit()
        db.close()

        flash('Part updated successfully.')
        return redirect(url_for('inventory'))

    db.close()
    return render_template('edit.html', part=part)


#Part Delete
@app.route('/delete/<int:part_id>')
def delete_part(part_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute(
        'DELETE FROM parts WHERE id = ? AND user_id = ?',
        (part_id, session['user_id'])
    )
    db.commit()
    db.close()

    flash('Part deleted.')
    return redirect(url_for('inventory'))

if __name__ == '__main__':
    app.run(debug=True)