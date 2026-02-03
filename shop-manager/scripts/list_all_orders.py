import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def list_all_orders():
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT order_id, description, completed FROM orders")
        rows = cursor.fetchall()
        if not rows:
            print("No orders found.")
            return

        for row in rows:
            order_id, description, completed = row
            status = "✅ Completed" if completed == 1 else "⏳ Pending"
            print(f"{status} Order ID: {order_id}, Description: {description}")
    except sqlite3.Error as e:
        print(f"Error listing all orders: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_all_orders()
