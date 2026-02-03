import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def list_active_queries():
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT query_id, customer, info FROM queries WHERE completed IS 0")
        rows = cursor.fetchall()
        if not rows:
            print("No unresolved queries found.")
            return

        print("Pk UNRESOLVED QUERIES:")
        for row in rows:
            query_id, customer, info = row
            print(f"Query ID: {query_id}, Customer: {customer}, Info: {info}")
    except sqlite3.Error as e:
        print(f"Error listing active queries: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_active_queries()
