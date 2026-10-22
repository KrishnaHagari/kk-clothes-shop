import sqlite3
DATABASE_NAME = "inventory.db"
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
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

if __name__ == "__main__":
    init_db()
    print("Database and Table created successfully")

