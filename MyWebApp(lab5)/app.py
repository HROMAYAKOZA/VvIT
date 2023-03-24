import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db", user="postgres", password="1234", host="localhost", port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if(username=='' or password==''): # пустое поле
                return render_template('login1.html')
            else:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                records = list(cursor.fetchall())
                if(records==[]): # пользователь не зарегистрирован
                    return render_template('login2.html')
                else:
                    print(records[0])
                    return render_template('account.html', full_name=records[0][1], login=records[0][2], pswrd=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if(login=='' or password=='' or name==''): # пустое поле
            return render_template('registration1.html')
        if " " in login or " " in password: # пробел в логине или пароле
            return render_template('registration3.html')
        else:
            cursor.execute("SELECT * FROM service.users WHERE login='%s'" % str(login))
            records = list(cursor.fetchall())
            if(records==[]): # пользователь не зарегистрирован
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                            (str(name), str(login), str(password)))
                conn.commit()
            else: # пользователь уже зарегистрирован
                print("works")
                return render_template('registration2.html')

        return redirect('/login/')

    return render_template('registration.html')
