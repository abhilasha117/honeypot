import sqlite3

conn = sqlite3.connect('honeypot.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM attempts'):
    print(row)
conn.close()