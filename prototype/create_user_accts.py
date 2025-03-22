#!/usr/bin/python
import sqlite3 as sql
from werkzeug.security import generate_password_hash

#This allows you the admin to create accounts manually through cli

email = input("Enter email: ")
password = input("Enter password: ")
admin = int(input("Is admin yes = 1 or no = 0: "))

hashed_password = generate_password_hash(password)
print(hashed_password)


con = sql.connect("users.db")
cur = con.cursor()
# Assuming your table 'User' has columns 'email', 'password', 'is_admin'
cur.execute("INSERT INTO Users (username, password, is_admin) VALUES (?, ?, ?)", (email, hashed_password, admin))
con.commit()
con.close(
