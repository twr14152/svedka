from flask import Flask, render_template, request
import sqlite3 as sql
from sqlite3 import Error
app = Flask(__name__)


conn = sql.connect('database.db')
print("DB openned successfully")

conn.execute("CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEST, email TEXT, password TEXT, operational_cost REAL)")
print("Table created successfully")
conn.close()

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/add')
def add():
   return render_template('add_user_form.html')

@app.route('/add_user',methods = ['POST', 'GET'])
def add_user():
   if request.method == 'POST':
      try:
         first_name = request.form['first_name']
         last_name = request.form['last_name']
         email = request.form['email']
         password = request.form['password']
         operational_cost = request.form['operational_cost']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user_data (first_name, last_name, email, password, operational_cost) VALUES (?,?,?,?,?)",(first_name, last_name, email, password, operational_cost))
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html",msg = msg)
         con.close()



@app.route('/list')
def list():
    try:
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM user_data ORDER BY id ASC")
            rows = cur.fetchall();
    except Error as e:
        rows = e
    finally:
        return render_template("list.html",rows = rows)


@app.route('/user')
def user():
    return render_template("user_info.html")


@app.route('/user/<id>', methods = ['POST','GET'])
def userId(id):
    try:
        id = request.form['id']
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            dbquery = f"SELECT operational_cost FROM user_data WHERE id={id}"
            print(dbquery)
            cur.execute(dbquery)
            rows = cur.fetchall()
    except Error as e:
        rows = e
    finally:
        return render_template("user_data_returned.html", rows = rows)


