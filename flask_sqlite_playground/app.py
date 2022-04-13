from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)


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
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO cb_inventory (id,desc,count,image_url) VALUES (?,?,?,?)",(id,desc,count,image_url))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
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




@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from cb_inventory")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


if __name__ == '__main__':
   app.run(debug = True)

