from flask import Flask, render_template, request
import sqlite3 as sql
from sqlite3 import Error
app = Flask(__name__)


conn = sql.connect('database.db')
print("DB openned successfully")

conn.execute("CREATE TABLE IF NOT EXISTS cb_inventory (id TEXT, desc TEXT, count INT, image_url TEXT,unit_price INT, notes TEXT)")
print("Table created successfully")
conn.close()


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/add')
def add():
   return render_template('new_item.html')

@app.route('/add_item',methods = ['POST', 'GET'])
def add_item():
   if request.method == 'POST':
      try:
         id = request.form['id']
         desc = request.form['desc']
         count = request.form['count']
         image_url = request.form['image_url']
         notes = request.form['notes']
         unit_price = request.form['unit_price']


         with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO cb_inventory (id,desc,count,image_url, unit_price, notes ) VALUES (?,?,?,?,?,?)",(id,desc,count,image_url,unit_price,notes))

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
                cur.execute("UPDATE cb_inventory SET id=? WHERE id=?",(new_id, id))
                con.commit()
                msg = "Inventory updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()




@app.route('/edit_count')
def edit_count():
    return render_template("edit_count.html")


@app.route('/edit_row_count/<id>', methods=['GET', 'POST'])
def edit_row_count(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            count=request.form['count']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE cb_inventory SET count=? WHERE id=?",(count, id))
                con.commit()
                msg = "Inventory updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()



@app.route('/edit_description')
def edit_description():
    return render_template("edit_description.html")


@app.route('/edit_row_description/<id>', methods=['GET', 'POST'])
def edit_row_description(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            desc=request.form['desc']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE cb_inventory SET desc=? WHERE id=?",(desc, id))
                con.commit()
                msg = "Inventory updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()

@app.route('/edit_image')
def edit_image():
    return render_template("edit_image.html")


@app.route('/edit_row_image/<id>', methods=['GET', 'POST'])
def edit_row_image(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            image_url=request.form['image_url']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE cb_inventory SET image_url=? WHERE id=?",(image_url, id))
                con.commit()
                msg = "Inventory updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()


@app.route('/edit_notes')
def edit_notes():
    return render_template("edit_notes.html")


@app.route('/edit_row_notes/<id>', methods=['GET', 'POST'])
def edit_row_notes(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            notes=request.form['notes']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE cb_inventory SET notes=? WHERE id=?",(notes, id))
                con.commit()
                msg = "Inventory updated successfully"
        except:
            con.rollback()
            msg = "Error updating table"

        finally:
            return render_template("result.html", msg = msg)
            con.close()



@app.route('/edit_price')
def edit_price():
    return render_template("edit_price.html")


@app.route('/edit_row_price/<id>', methods=['GET', 'POST'])
def edit_row_price(id):
    if request.method=='POST':
        try:
            id=request.form['id']
            unit_price=request.form['unit_price']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("UPDATE cb_inventory SET unit_price=? WHERE id=?",(unit_price, id))
                con.commit()
                msg = "Inventory updated successfully"
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
                cur.execute("DELETE FROM cb_inventory WHERE id=?", [id])
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
        cur.execute("SELECT * FROM cb_inventory ORDER BY id ASC")
        #cur.execute("select * from cb_inventory")
        rows = cur.fetchall();
    except Error as e:
        rows = e
    finally:
        return render_template("list.html",rows = rows)


if __name__ == '__main__':
   app.run(debug = True)

