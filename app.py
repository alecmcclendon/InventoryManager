# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Step 1: Connect to the database (or create it)
def get_db_connection():
    conn = sqlite3.connect('inventory.db')  # Creates DB file if it doesn't exist
    conn.row_factory = sqlite3.Row          # Allows us to use column names
    return conn

# Step 2: Create the products table if it doesn't exist yet
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_number INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL,
            description TEXT,
            stock INTEGER NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            added_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Step 3: Home page – show product list
@app.route('/')
def index():
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', '')

    conn = get_db_connection()

    # Start with base SQL and parameter list
    sql = "SELECT * FROM products"
    params = []

    # Search logic
    if search:
        sql += " WHERE name LIKE ? OR item_number LIKE ? OR category LIKE ?"
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])

    # Sort logic
    if sort == "date_desc":
        sql += " ORDER BY added_date DESC"
    elif sort == "date_asc":
        sql += " ORDER BY added_date ASC"
    elif sort == "price_asc":
        sql += " ORDER BY price ASC"
    elif sort == "price_desc":
        sql += " ORDER BY price DESC"
    elif sort == "stock_desc":
        sql += " ORDER BY stock DESC"
    elif sort == "stock_asc":
        sql += " ORDER BY stock ASC"
    elif sort == "item_asc":
        sql += " ORDER BY CAST(item_number AS INTEGER) ASC"
    elif sort == "item_desc":
        sql += " ORDER BY CAST(item_number AS INTEGER) DESC"
    elif sort == "":  # "なし" selected
        pass  # no sorting added
    else:
        sql += " ORDER BY added_date DESC"  # Default fallback

    # Final SQL execution
    products = conn.execute(sql, params).fetchall()
    conn.close()

    return render_template('index.html', products=products, search=search, sort=sort)

# Step 4: Add new product
@app.route('/add', methods=['POST'])
def add():
    item_number = request.form['item_number']
    name = request.form['name']
    description = request.form['description']
    stock = request.form['stock']
    price = request.form['price']
    category = request.form['category']
    added_date = request.form['added_date']

    conn = get_db_connection()

    # Check for duplicates BEFORE inserting
    existing = conn.execute('SELECT * FROM products WHERE item_number = ?', (item_number,)).fetchone()

    if existing:
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return render_template('index.html', products=products, search="", error="この商品はもう追加されました")

    # Safe to insert
    conn.execute('INSERT INTO products (item_number, name, description, stock, price, category, added_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (item_number, name, description, stock, price, category, added_date))
    conn.commit()
    conn.close()
    return redirect('/')

# --------------------------------------------------------------------

    # 消すため
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


# ---------------------------------------------------------------------

# 編集のため

# Step 5: Edit page – show form with current values
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', product=product)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    item_number = request.form['item_number']
    name        = request.form['name']
    description = request.form['description']
    stock       = request.form['stock']
    price       = request.form['price']
    category    = request.form['category']
    added_date  = request.form['added_date']

    conn = get_db_connection()
    conn.execute('''
        UPDATE products
        SET item_number = ?, name = ?, description = ?, stock = ?, price = ?, category = ?, added_date = ?
        WHERE id = ?
    ''', (item_number, name, description, stock, price, category, added_date, id))
    conn.commit()
    conn.close()
    return redirect('/')
    
# Initialize the DB and run the app
if __name__ == '__main__':
    init_db()  # Make sure DB exists before app runs
    app.run(debug=True, port=5000)



#  code to reset sql
# ---------------------
# rm inventory.db
# python app.py
