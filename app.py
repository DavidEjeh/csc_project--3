from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random value

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    admin = cur.fetchone()
    cur.close()
    conn.close()
    if admin:
        session['admin_logged_in'] = True
        return redirect('/view')
    else:
        flash('Invalid username or password!')
        return redirect('/')


# Logout route
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_clothes():
    if not session.get('admin_logged_in'):
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        size = request.form['size']
        color = request.form['color']
        price = request.form['price']
        description = request.form['description']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO clothes (name, brand, size, color, price, description) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, brand, size, color, price, description))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/view')
    return render_template('add_clothes.html')

@app.route('/view')
def view_clothes():
    if not session.get('admin_logged_in'):
        return redirect('/')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clothes")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('view_clothes.html', clothes=data)

if __name__ == '__main__':
    app.run(debug=True)