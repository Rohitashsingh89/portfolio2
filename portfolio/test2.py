from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rohitashsingh'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        # email = request.form['email']
        # password = request.form['password']
        # phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO CONTACT(fname, lname) VALUES(%s, %s)", (fname, lname))
        # cur.execute("INSERT INTO CONTACT VALUES(fname, lname, email, password)")
        mysql.connection.commit()
        cur.close()
        return 'success'
        # entry = Contact(name=name, email=email, phone_num=phone, msg=Message)
        # db.session.add(entry)
        # db.session.commit()
    return render_template('rendom.html')
    

if __name__ == "__main__":
    app.run()