from __future__ import print_function
from flask import Flask, render_template, request, session, redirect, g, url_for, jsonify
import os
import psycopg2
import pandas as pd


app = Flask(__name__)

app.secret_key = os.urandom(24)

# DATABASE CONNECTION
conn = psycopg2.connect(
    host='crayon-pipeline.postgres.database.azure.com',
    database='postgres',
    user='crayon@crayon-pipeline',
    password='saturam_12345',
    port=5432)

# DATA RETRIEVE
query = pd.read_sql_query('SELECT username, password, access FROM mrf.temp_user', conn)
df = pd.DataFrame(query, columns=['username', 'password', 'access'])
conn.close()


# CHECK PASSWORD
def authorise(uname, password):
    access = 0
    pwd = df['password'][df['username'] == uname].values
    if pwd[0] == password:
        access = df['access'][df['username'] == uname].values
    return int(access[0])


# LOGIN PAGE
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('user', None)
        user_access = authorise(request.form['uname'], request.form['pass'])
        if user_access:
            # STORE USER DATA
            session['access'] = user_access
            session['user'] = request.form['uname']
            # REDIRECT TO HOME
            return redirect(url_for('home'))
    return render_template('login.html')


# HOME PAGE
@app.route('/home')
def home():
    if g.user:
        # DISPLAY HOME PAGE
        return render_template('home.html', user=session['user'], access=session['access'])
    return redirect(url_for('login'))


# WELCOME PAGE
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if g.user:
        # DISPLAY WELCOME PAGE
        return render_template('welcome.html', user=session['user'], access=session['access'])
    return redirect(url_for('login'))


# API TO GET USER INPUTS
@app.route('/calc', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        # REDIRECT TO DISPLAY RESULTS
        return redirect(url_for('add'))

    if g.user:
        return render_template('calculate.html', user=session['user'], access=session['access'])

    return redirect(url_for('login'))


# API TO PERFORM CALCULATION
@app.route('/add', methods=['GET', 'POST'])
def add():
    if g.user and request.method == 'POST':
        # REDIRECT TO DISPLAY RESULTS
        return render_template('process.html', user=session['user'], access=session['access'],
                               value1=int(request.form['num1']), value2=int(request.form['num2']),
                               operator=request.form['operator'])
    else:
        return redirect(url_for('login'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


# DROP THE USER WHEN LOGGED OUT
@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
