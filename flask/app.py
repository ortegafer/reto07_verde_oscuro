from flask import Flask, render_template, request, redirect, url_for, session
import os
import sys
import sqlite3
import pandas as pd
import plotly.express as px
import importlib.util
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__)

app.secret_key = 'jjjjj'
login_manager = LoginManager()
login_manager.init_app(app)


db_path = "calculos.db"
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT,
                    salario REAL,
                    edad INTEGER,
                    años_trabajados INTEGER,
                    resultado REAL
                )''')
    conn.commit()
    conn.close()
init_db()


def importar_modulo(ruta, nombre_modulo):
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

finanzas1 = importar_modulo('flask/static/scripts/Funcion_Finanzas1.py', 'finanzas1')
finanzas2 = importar_modulo('flask/static/scripts/Funcion_Finanzas2.py', 'finanzas2')


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    users = {"admin": User("admin", "admin"), "user": User("user", "user")}
    return users.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            login_user(User("admin", "admin"))
            return redirect(url_for('admin_dashboard'))
        elif username == 'user' and password == 'user':
            login_user(User("user", "user"))
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/calcular_trabajador', methods=['GET','POST'])

def calcular_trabajador():
    resultado = None  
    if request.method == 'POST':
        print(request.form)
        salario = float(request.form['salario'])
        edad = int(request.form['edad_actual'])
        años_trabajados = int(request.form['años_trabajados'])
        interes1 = float(request.form['interes_ahorro'])
        interes2 = float(request.form['interes_renta'])
        resultado = finanzas1.calcular_primas_jubilacion(salario, edad, años_trabajados, interes1, interes2, duración_interes1, interes_rendimiento1, interes_rendimiento2, duración_interés_rendimiento1,fecha_jubilacion)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO calculos (usuario, salario, edad, años_trabajados, resultado) VALUES (?, ?, ?, ?, ?)",
                  (current_user.username, salario, edad, años_trabajados, resultado))
        conn.commit()
        conn.close()

    return render_template('trabajador_calculadora.html', resultado=resultado)

@app.route('/calcular_csv', methods=['GET','POST'])

def calcular_csv():
    resultado_csv = None
    if request.method == 'POST':
        archivo = request.files['archivo']
        if archivo:
            if archivo.filename.endswith('.csv'):
                df = pd.read_csv(archivo)
            elif archivo.filename.endswith('.xlsx'):
                df = pd.read_excel(archivo, engine='openpyxl')
            else:
                return "Formato no soportado"
            
            resultado_csv = finanzas2.calcular_primas_jubilacion_df(df)
            resultado_csv = df.to_html()
    
    return render_template('csv_calculadora.html', resultado_csv=resultado_csv)

@app.route('/admin')

def admin_dashboard():
    if current_user.username != "admin":
        return redirect(url_for('index'))
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM calculos", conn)
    conn.close()
    
    fig = px.bar(df, x='usuario', y='resultado', title='Resultados de Cálculos')
    graph_html = fig.to_html(full_html=False)
    
    return render_template('admin.html', tabla=df.to_html(), grafico=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
