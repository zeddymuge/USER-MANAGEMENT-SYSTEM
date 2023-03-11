from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import re

#current module
app = Flask(__name__)
app.secret_key = 'wnsjxn12@jk'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'manager'

mysql = MySQL(app) 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM manage WHERE email = % s AND password = % s', (email, password, ))
    
        user = cur.fetchone()
        cur.close()
        if user:
            session['loggedin'] = True
            session['email'] = user[4]
            session['password'] = user[5]
            message = 'Logged in successfully!'
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM manage')
            userDetails = cur.fetchall()
            cur.close()
            return render_template('user.html', userDetails=userDetails, message=message)
    
        else:
            message = 'Email not found or incorrect password'

    return render_template('login.html', message = message)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    userDetails = request.form
    if request.method == 'POST' and 'f_name' in userDetails and 'l_name' in userDetails and 'password' in userDetails and 'email' in userDetails:
        
        first_name = userDetails['f_name']
        last_name = userDetails['l_name']
        email = userDetails['email']
        password = userDetails['password']
        role = userDetails['role']
        country = userDetails['country']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM manage WHERE email = % s', (email, ))
        account = cur.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not first_name or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cur.execute("INSERT INTO manage (id,first_name, last_name, email, password, role, country) VALUES(NULL, %s, %s, %s, %s, %s, %s)",( first_name, last_name, email, password, role, country))
            mysql.connection.commit()
            cur.close()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
        return(mesage)
            
    return render_template('register.html',  mesage = mesage)
 
@app.route('/user')
def user():
   
    cur = mysql.connection.cursor()
    results = cur.execute("SELECT * FROM manage ")
    userDetails = cur.fetchall()
    cur.close()
    if results > 0:
        return render_template("user.html", userDetails=userDetails)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST' and 'f_name' in request.form and 'l_name' in request.form and 'email' in request.form and 'password' in request.form and 'role' in request.form and 'country' in request.form:
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        country = request.form['country']
        cur.execute("UPDATE manage SET first_name=%s, last_name=%s, email=%s, password=%s, role=%s, country=%s WHERE id=%s", (first_name, last_name, email, password, role, country, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('user'))

    cur.execute('SELECT * FROM manage WHERE id = %s', (id,))
    user = cur.fetchone()
    cur.close()
    return render_template('edit.html', user=user)


@app.route('/delete/<int:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM manage WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('user'))
    



if __name__ == '__main__':
    app.run(debug=True)