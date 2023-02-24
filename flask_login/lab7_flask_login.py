# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:34:22 2022

@author: Andrew
"""

from datetime import datetime
import re
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors



# =============================================================================
# To setup the Flask:
#     On PowerShell input the commands:
#         Goto the directory this python file is at:
#
#           > cd [path to folder with this file]
#           > py -3 -m venv venv #Creates a virtual environment folder named venv
#           > venv\Scripts\activate #Activates the virtual environment
#         Setting the flask:
#
#           > '$env:FLASK_APP = lab7_flask_login.py'
#           > pip install flask
#
#
# To run the website:
#     1. Open powershell
#     2. Goto directory of this file:
#
#       Documents\\UMGC\\SDEV3_300_Building_Secure_Python_Applications\\
#       Lab_Assignments\\Lab7_Flask_Login\\flask_login
#
#    3. Enter the following:
#
#       > 'flask run'
#       or
#       >'flask run --host=0.0.0.0' #This is to make server publicly available.
#
#    4. Open browser and goto IP shown in the powershell:
#        typically 127.0.0.1:5000
# =============================================================================




app = Flask(__name__, template_folder = 'TemplateFiles',
            static_folder = 'StaticFiles')

cdate = datetime.now().strftime("%a %b %d, %Y %I:%M %p")
                                #Tue Sep 20, 2022 09:00:00 AM

# =============================================================================
# For the database used to store the login information, I used MySQL.
# Installed MySQL from dev.mysql.com/downloads
#
# From the PowerShell I install flask_mysqldb:
#       > pip install mysqlclient
#       > pip install flask-mysqldb
#
# =============================================================================

app.secret_key = 'key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*i52mzLq'
app.config['MYSQL_DB'] = 'zoeysitelogin'

mysql = MySQL(app)

# =============================================================================
# LOGIN
# =============================================================================
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    When a form for logging in is submit (includes username & password), then
    check the form input to see if it matches with the information in the
    MySQL database.

    Cursor is used to search for the specified variables given in the database.

    If an account was properly fetched, then set the id and username of the
    account to the session on the website.

    Actions done during that session will be linked to the user id.

    Returns
    -------
    TYPE
        Goto home page of the website as the new session.

    """
    msg = ''
    if (request.method == 'POST' and 'username' in request.form and 'password'
        in request.form):

        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s'
                       +' AND password = %s', (username, password, ))

        account = cursor.fetchone()
        if not account: #If account matches with db info, log user in for the session.
            msg = 'Incorrect username/password!'

        else:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in Successfully!'

            return render_template('index.html', msg = msg)

    return render_template('login.html', msg = msg)


# =============================================================================
# LOGOUT
# =============================================================================
@app.route('/logout')
def logout():
    """
    Remove the values from their assigned variables, then return None as the
    value for the assigned variables.

    Returns
    -------
    TYPE
        Sends user to the login page and updating the session.

    """
    session.pop('loggedin', None) #Remove the value in loggedin and return None.
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))


# =============================================================================
# REGISTER
# =============================================================================
@app.route('/register', methods = ['GET', 'POST'])
def register():
    """
    This function works similar to the login function.
    Take the form input and check to see if it matches with the data in the
    database.
    If it matches, then registration fails.
    If it does not match, then create the new account if the input is proper.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    msg = ''
    if (request.method == 'POST' and 'username' in request.form and 'password'
        in request.form and 'email' in request.form):

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s', (username, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            #RegEx:[Any characters not @] @ [Any characters not @] . [any characters not @]
            msg = 'Invalid email address!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            #RegEx: [Only letters and numbers]
            msg = 'Username must contain only letters and numbers!'

        elif not re.match(r'(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$!])[\w\d@#$!].{12,40}'
                          , password):
            msg = ('Password must contain at least one number, lowercase letter'+
                ', uppercase, special character, and atleast 12 characters long!')

        elif not username or not password or not email:
            msg = 'Please fill out the form!'

        else:
            #The order of the inputs is important.
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)',
                           (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg = msg)




# =============================================================================
# INDEX PAGE
# =============================================================================

@app.route('/index.html')
def index():
    """
    Home page

    Returns
    -------
    TYPE
        The link to the page.

    """

    return render_template('index.html', date = cdate)
    #date is called from the HTML by: {{date}}.

@app.route('/zoey_gallery.html')
def zoey_gallery():
    """
    Gallery page

    Returns
    -------
    TYPE
        The link to the page.

    """
    return render_template('zoey_gallery.html', date = cdate)

@app.route('/zoey_about.html')
def zoey_about():
    """
    About page

    Returns
    -------
    TYPE
        The link to the page.

    """
    return render_template('zoey_about.html', date = cdate)

@app.route('/zoey_contact_us.html')
def zoey_contact_us():
    """
    Contact Us page

    Returns
    -------
    TYPE
        The link to the page.

    """
    return render_template('zoey_contact_us.html', date = cdate)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
