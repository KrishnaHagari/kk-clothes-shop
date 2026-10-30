import sqlite3

DATABASE_NAME = "inventory.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # ಡಿಕ್ಷನರಿ ರೀತಿಯಲ್ಲಿ ಡೇಟಾ ಪಡೆಯಲು
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Products ಟೇಬಲ್
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            size TEXT NOT NULL,
            cost_price REAL NOT NULL,
            selling_price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    # 2. Sales 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            item_name TEXT,
            cost_price REAL,
            selling_price REAL,
            profit REAL,
            sold_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_product_to_db(item_name, category, size, cost_price, selling_price, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the product already exists (case-insensitive and trimmed)
    cursor.execute("""
        SELECT id, quantity FROM products 
        WHERE LOWER(TRIM(item_name)) = LOWER(TRIM(?)) 
          AND LOWER(TRIM(category)) = LOWER(TRIM(?)) 
          AND LOWER(TRIM(size)) = LOWER(TRIM(?))
    """, (item_name, category, size))
    existing_item = cursor.fetchone()

    if existing_item:
        # add the new quantity to the existing quantity
        new_quantity = existing_item["quantity"] + quantity
        cursor.execute("""
            UPDATE products 
            SET quantity = ?, cost_price = ?, selling_price = ?
            WHERE id = ?
        """, (new_quantity, cost_price, selling_price, existing_item["id"]))
    else:
        
        cursor.execute("""
            INSERT INTO products (item_name, category, size, cost_price, selling_price, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (item_name, category, size, cost_price, selling_price, quantity))

    conn.commit()
    conn.close()

def get_all_products(search: str = "", category: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    # Search filter
    search = search.strip() if search else ""
    if search:
        query += " AND LOWER(item_name) LIKE LOWER(?)"
        params.append(f"%{search}%")

    # Category filter
    category = category.strip() if category else ""
    if category and category.lower() != "all":
        query += " AND LOWER(TRIM(category)) = LOWER(TRIM(?))"
        params.append(category)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def sell_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the product exists and has quantity > 0
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if product and product["quantity"] > 0:
        cost = float(product["cost_price"])
        selling = float(product["selling_price"])
        profit = round(selling - cost, 2)

        # Update the product quantity and insert into sales table in a single transaction
        cursor.execute(
            "UPDATE products SET quantity = quantity - 1 WHERE id = ?",
            (product_id,)
        )

        
        cursor.execute(
            """
            INSERT INTO sales (product_id, item_name, cost_price, selling_price, profit)
            VALUES (?, ?, ?, ?, ?)
            """,
            (product_id, product["item_name"], cost, selling, profit)
        )

        conn.commit()

    conn.close()

def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_sales_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_sales_count,
            COALESCE(SUM(profit), 0) as total_profit
        FROM sales
    """)
    row = cursor.fetchone()
    conn.close()

    return {
        "total_sales_count": row["total_sales_count"],
        "total_profit": round(row["total_profit"], 2)
    }

def get_recent_sales(limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, item_name, cost_price, selling_price, profit, sold_at 
        FROM sales 
        ORDER BY id DESC 
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_product_by_id(product_id: int):
     
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_product_in_db(product_id: int, item_name: str, category: str, size: str, cost_price: float, selling_price: float, quantity: int):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products 
        SET item_name = ?, category = ?, size = ?, cost_price = ?, selling_price = ?, quantity = ?
        WHERE id = ?
    """, (item_name, category, size, cost_price, selling_price, quantity, product_id))
    conn.commit()
    conn.close()

def get_all_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Initialize the database
init_db()