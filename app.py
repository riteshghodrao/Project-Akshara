from flask import Flask, render_template,request,json,flash
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import sqlite3 as sql
app= Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
"""app.config['MYSQL_DATABASE_USER'] = 'ritesh29'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ritesh29'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'"""
mysql.init_app(app)
conn = sql.connect('database.db')
print "Opened database successfully";
#conn.execute('DROP TABLE IF EXISTS students')
#conn.execute('CREATE TABLE students (ID Integer PRIMARY KEY AUTOINCREMENT,sn TEXT, dd TEXT, topic TEXT, description TEXT, remark TEXT, vn TEXT)')
#print "Table created successfully";

conn.close()

@app.route("/")
def main():
    return render_template('add.html')

@app.route('/add')
def new_add():
    return render_template('add.html')


"""@app.route('/signIn', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == 'POST':
                if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                        error = 'Invalid Credentials. Please try again.'
                else:
                        return redirect(url_for('home'))
        return render_template('signin.html', error=error)"""

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
     if request.method == 'POST':
                try:
                    sn = request.form['sn']
                    dd = request.form['dd']
                    vn = request.form['vn']
                    remark = request.form['remark']
                    topic = request.form['topic']
                    description = request.form['description']
                    print("done1")
                    with sql.connect("database.db") as con:
                            cur = con.cursor()
                            print("done2")
                            cur.execute("INSERT INTO students (sn,dd,topic,description,remark,vn) VALUES (?,?,?,?,?,?)",(sn,dd,topic,description,remark,vn) )
                            print("done3")
                            con.commit()
                            flash("Record successfully added")
                            #print("haha")
                except:
                    con.rollback()
                    flash("error in insert operation")
                    #print("lag gaye")
            
                finally:
                    con = sql.connect("database.db")
                    con.row_factory = sql.Row
                    cur = con.cursor()
                    cur.execute("select * from students")
                    rows = cur.fetchall();


                    return render_template("list.html",rows=rows)
                    con.close()
@app.route('/search')
def list():
     con = sql.connect("database.db")
     con.row_factory = sql.Row
     
     cur = con.cursor()
     cur.execute("select * from students")
     
     rows = cur.fetchall();
     return render_template("list.html",rows = rows)

@app.route('/delete')
def delete():
    return render_template('delete1.html')


@app.route('/search_item',methods=['GET','POST'])
def search_item():
    if request.method=='POST':
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        if(True):
            s_name = request.form['s_name']
            s_date = request.form['s_date']
            s_topic = request.form['s_topic']

            
            cur = con.cursor()
            print('hahalol')
                #print(s_name)
            cur.execute("SELECT * FROM students where sn = ? or dd = ? or topic = ?",(s_name,s_date,s_topic,))
            rows = cur.fetchall();
            return render_template("list.html",rows = rows)
            con.close()

@app.route('/delete_item',methods=['GET','POST'])
def delete_item():
    if request.method=='POST':
        try:
            d_id = request.form['d_id']
            

            with sql.connect("database.db") as con:
                cur = con.cursor()
                print('hahalol')
                #print(s_name)
                cur.execute("DELETE FROM students where ID = ? ",(d_id,))
                con.commit()
        except:
            con.rollback()
        finally:
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from students")
            rows = cur.fetchall();
            return render_template("list.html",rows=rows)
            con.close()
            


if __name__ == "__main__":
    app.run(debug=True)
    