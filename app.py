from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re  
  
app = Flask(__name__)
app.secret_key = 'register'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        if 'first_name' in request.form and 'last_name' in request.form and 'phone_number' in request.form and 'email' in request.form:
            firstName = request.form['first_name']
            lastName = request.form['last_name']
            phone_number = request.form['phone_number']
            email = request.form['email']
            
            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
                account = cursor.fetchone()
            except Exception as e:
                print("ERROR FOR DB CONNECTION")
                message = "ERROR FOR DB CONNECTION"
                
                return render_template('register.html', message = message)
            
            if account:
                message = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Invalid email address !'
            elif not firstName or not lastName or not phone_number or not email:
                message = 'Please fill out the form !'
            else:
                cursor.execute('INSERT INTO user VALUES (% s, % s, % s, % s)', (firstName, lastName, email, phone_number, ))
                mysql.connection.commit()
                
                message = 'You have successfully registered !'
        else:
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    else:
        message = 'Please send true type request for registeration'
        
    return render_template('register.html', message = message)
    
if __name__ == "__main__":
    app.run(debug=True)
