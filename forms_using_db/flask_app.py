from flask import Flask, render_template, request
import sqlite3 as sql
from sqlite3 import Error
app = Flask(__name__)


conn = sql.connect('database.db')
print("DB openned successfully")

conn.execute("CREATE TABLE IF NOT EXISTS user_info (id TEXT, monthly_expenses INT)")
print("Table created successfully")
conn.close()


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/add')
def add():
   return render_template('add_client.html')

@app.route('/add_item',methods = ['POST', 'GET'])
def add_item():
   if request.method == 'POST':
      try:
         id = request.form['id']
         monthly_expenses = request.form['monthly_expenses']


         with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO user_info (id,monthly_expenses) VALUES (?,?)",(id,monthly_expenses))

            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html",msg = msg)
         con.close()



@app.route('/edit_id')
def edit_id():
    return render_template("edit_id.html")


@app.route('/edit_row_id/<id>', methods=['GET', 'POST'])
def edit_row_id(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            new_id=request.form['new_id']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE user_info SET id=? WHERE id=?",(new_id, id))
                con.commit()
                msg = "Updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()




@app.route('/edit_monthly_expenses')
def edit_monthly_expenses():
    return render_template("edit_monthly_expenses.html")


@app.route('/edit_row_monthly_expenses/<id>', methods=['GET', 'POST'])
def edit_row_monthly_expenses(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            monthly_expenses=request.form['monthly_expenses']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE user_info SET monthly_expenses=? WHERE id=?",(monthly_expenses, id))
                con.commit()
                msg = "Updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()

###########


@app.route('/del_id')
def del_id():
    return render_template("del_id.html")


@app.route('/del_row_id/<id>', methods=['GET','POST'])
def del_row_id(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("DELETE FROM user_info WHERE id=?", [id])
                con.commit()
                msg = "item deleted..."
        except Error as e:
            con.rollback()
            msg = e

        finally:
            return render_template("result.html", msg = msg)
            con.close()


@app.route('/list')
def list():
    try:
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM user_info ORDER BY id ASC")
        #cur.execute("select * from user_info")
        rows = cur.fetchall();
    except Error as e:
        rows = e
    finally:
        return render_template("list.html",rows = rows)


if __name__ == '__main__':
   app.run(debug = True)
