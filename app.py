from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import init_db, get_db
from werkzeug.security import  generate_password_hash, check_password_hash
from logic import get_low_stock_parts
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = 'abdu1234'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
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


#inventory route

@app.route('/inventory')
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '').strip()
    filter_category = request.args.get('category', '')
    filter_type = request.args.get('part_type', '')

    query = 'SELECT * FROM parts WHERE user_id = ?'
    params = [session['user_id']]

    if search:
        query += ' AND (name LIKE ? OR brand LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    if filter_category:
        query += ' AND category = ?'
        params.append(filter_category)

    if filter_type:
        query += ' AND part_type = ?'
        params.append(filter_type)

    query += ' ORDER BY name ASC'

    db = get_db()
    parts = db.execute(query, params).fetchall()

    stats = db.execute('''
        SELECT 
            COUNT(*) as total_parts,
            SUM(quantity) as total_units,
            COUNT(DISTINCT category) as total_categories,
            SUM(price * quantity) as total_value
        FROM parts 
        WHERE user_id = ?
    ''', (session['user_id'],)).fetchone()

    db.close()

    low_stock = get_low_stock_parts(parts)

    return render_template('inventory.html',
        parts=parts,
        username=session['username'],
        low_stock_count=len(low_stock),
        stats=stats,
        search=search,
        filter_category=filter_category,
        filter_type=filter_type
    )


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
        part_type = request.form['part_type']
        brand = request.form['brand']
        serial_number = request.form['serial_number'] or None
        price = float(request.form['price'])
        threshold = int(request.form['threshold'])

        db.execute(
            '''UPDATE parts 
               SET name=?, quantity=?, category=?, part_type=?, brand=?, serial_number=?, price=?, low_stock_threshold=?
               WHERE id=? AND user_id=?''',
            (name, quantity, category, part_type, brand, serial_number, price, threshold, part_id, session['user_id'])
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


    @app.context_processor
    def inject_user():
        return dict(session=session)