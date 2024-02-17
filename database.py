import sqlite3

def main():
    conn = sqlite3.connect("second.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM Rests")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()

main()