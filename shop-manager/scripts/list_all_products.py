import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def list_all_products():
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, name, price, info FROM products")
        rows = cursor.fetchall()
        if not rows:
            print("No products found.")
            return

        print("--- ALL PRODUCTS ---")
        for row in rows:
            product_id, name, price, info = row
            print(f"Product ID: {product_id}, Name: {name}, Price: {price}, Info: {info}")
    except sqlite3.Error as e:
        print(f"Error listing all products: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_all_products()
