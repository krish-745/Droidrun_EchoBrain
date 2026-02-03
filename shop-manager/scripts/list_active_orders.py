import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def list_active_orders():
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT order_id, description FROM orders WHERE completed IS 0")
        rows = cursor.fetchall()
        if not rows:
            print("No active orders found.")
            return

        print("⏳ PENDING ORDERS:")
        for row in rows:
            order_id, description = row
            print(f"Order ID: {order_id}, Description: {description}")
    except sqlite3.Error as e:
        print(f"Error listing active orders: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_active_orders()
