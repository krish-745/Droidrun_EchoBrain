import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

def resolve_query(query_id):
    db_path = r"C:\Users\krish\OneDrive\Documents\droidrun\brain.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE queries SET completed = 1 WHERE query_id = ?", (query_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"✅ Query ID {query_id} marked as resolved.")
        else:
            print(f"Query ID {query_id} not found or already resolved.", file=sys.stderr)
    except sqlite3.Error as e:
        print(f"Error resolving query: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        resolve_query(int(sys.argv[1]))
    else:
        print("Usage: python resolve_query.py <query_id>", file=sys.stderr)
