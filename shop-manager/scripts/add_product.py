import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def add_product(name, price, info):
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, info) VALUES (?, ?, ?)", (name, price, info))
        conn.commit()
        print("✅ Added product")
    except sqlite3.Error as e:
        print(f"Error adding product: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        add_product(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python add_product.py <name> <price> <info>", file=sys.stderr)
