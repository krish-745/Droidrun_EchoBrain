import sqlite3
import datetime

class Database:
    def __init__(self,db_name="brain.db"):
        self.db_name=db_name
        self.init()
        
    def init(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS owner (
                            name TEXT,
                            mobile_number INTEGER UNIQUE)''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS products (
                            product_id INTEGER PRIMARY KEY,
                            name TEXT,
                            price TEXT,
                            info TEXT)''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS orders (
                            order_id INTEGER PRIMARY KEY,
                            customer TEXT,
                            description TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS queries (
                            query_id INTEGER PRIMARY KEY,
                            customer TEXT,
                            timestamp DATETIME,
                            type TEXT,
                            info TEXT)''')
            
            conn.commit()
                    
    def get_context(self):
        with sqlite3.connect(self.db_name) as conn:
            owner = conn.execute("SELECT name FROM owner LIMIT 1").fetchone()
            biz_name = owner[0] if owner else "My Business"
            cursor = conn.execute("SELECT name, price, info FROM products")
            rows = cursor.fetchall()
            if not rows:
                inventory = "INVENTORY: [No products added yet]"
            else:
                text_list = [f"- {r[0]}: {r[1]} ({r[2]})" for r in rows]
                inventory = "PRODUCT LIST:\n" + "\n".join(text_list)
            return biz_name, inventory
    
    def log_sale(self, handle, item_name):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO orders (customer, description) VALUES (?, ?)", 
                         (handle, item_name))
            conn.commit()
    
    def log_query(self, handle, category, info):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO queries (customer, type, info, timestamp) VALUES (?, ?, ?, ?)", 
                         (handle, category, info, ts))
            conn.commit()
            
    