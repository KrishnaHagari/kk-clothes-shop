import sqlite3
DATABASE_NAME = "inventory.db"
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # ಈ ಸಾಲು ಇರಲೇಬೇಕು!
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    size TEXT NOT NULL,
    cost_price REAL NOT NULL,
    selling_price REAL NOT NULL,
    quantity INTEGER NOT NULL)
    """)
    conn.commit()
    conn.close()

def add_product_to_db(item_name,category,size,cost_price,selling_price,quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO products(item_name, category, size, cost_price, selling_price, quantity)
    VALUES(?,?,?,?,?,?)
    """, (item_name, category, size, cost_price, selling_price, quantity))
    conn.commit()
    conn.close()

def get_all_products(search: str = "", category: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    #(Search filter)
    if search:
        query += " AND item_name LIKE ?"
        params.append(f"%{search}%")

    #(Category filter)
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def sell_product(product_id:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = quantity - 1 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def delete_product(product:int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database and Table created successfully")

