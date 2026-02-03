import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def complete_order(order_id):
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET completed = 1 WHERE order_id = ?", (order_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ Order ID {order_id} marked as completed.")
        else:
            print(f"Order ID {order_id} not found or already completed.", file=sys.stderr)
    except sqlite3.Error as e:
        print(f"Error completing order: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        complete_order(int(sys.argv[1]))
    else:
        print("Usage: python complete_order.py <order_id>", file=sys.stderr)
