from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/dibujo")
def dibujo():
    return render_template('dibujo.html')


@app.route('/datos', methods=['GET', 'POST'])
def datos():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            fichero = file.filename.replace('.csv','')
            return render_template('table.html', fichero = fichero, data=df.to_html())
    return render_template('datos.html')

if (__name__ == "__main__"):
    app.run(debug=True)