import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def list_all_queries():
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT query_id, customer, info, completed FROM queries")
        rows = cursor.fetchall()
        if not rows:
            print("No queries found.")
            return

        for row in rows:
            query_id, customer, info, completed = row
            status = "✅ Resolved" if completed == 1 else "Pk Pending"
            print(f"{status} Query ID: {query_id}, Customer: {customer}, Info: {info}")
    except sqlite3.Error as e:
        print(f"Error listing all queries: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_all_queries()
