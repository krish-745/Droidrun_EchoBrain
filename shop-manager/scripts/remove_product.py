import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def remove_product(product_id):
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ Product ID {product_id} removed successfully.")
        else:
            print(f"Product ID {product_id} not found.", file=sys.stderr)
    except sqlite3.Error as e:
        print(f"Error removing product: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        remove_product(int(sys.argv[1]))
    else:
        print("Usage: python remove_product.py <product_id>", file=sys.stderr)
