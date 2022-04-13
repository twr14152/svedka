import sqlite3

conn = sqlite3.connect('database.db')
print("DB openned successfully")

conn.execute("CREATE TABLE IF NOT EXISTS cb_inventory (id TEXT, desc TEXT, count INT, image_url TEXT)")
print("Table created successfully")
conn.close()

