from flask import Flask, render_template, request
import pandas as pd
import pickle
import math
import datetime as dt

app = Flask(__name__)

# Cargar modelo de predicción
with open("notebooks/Data Mining/modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

def calculo_nomina(salario_actual, años_hasta_jubilación, ipc):
    redondeado = math.floor(años_hasta_jubilación)
    salario = salario_actual
    for i in range(0, redondeado):
        salario = salario + salario * ipc.iloc[i, 1]
    return float(salario)

def calcular_monto_mensual(capital, intereses):
    sum = 0
    for i in range(len(intereses)):
        num = 1
        for j in range(0, len(intereses[:i+1])):
            num *= (1 + intereses[j]) ** (-1)
        sum += num
    
    monto = capital / sum
    return monto

def calcular_primas_jubilacion(salario, edad, años_trabajados, interes1, interes2, duración_interes1, interes_rendimiento1, interes_rendimiento2, duración_interés_rendimiento1):
    import datetime as dt
    import pandas as pd
    import pickle
    with open("notebooks/Data Mining/modelo.pkl", "rb") as f:
        modelo = pickle.load(f)

    X_pred = pd.DataFrame({'Edad': [edad], 'Ingreso Anual (€)': [salario]})
    años_hasta_jubilacion = modelo.predict(X_pred)[0]  # Predecimos los años hasta la jubilación
    fecha_jubilacion = dt.date(2025, 1, 1) + dt.timedelta(days=años_hasta_jubilacion * 365)
        
    ipc_data = pd.read_excel('Datos/Originales/Dataset_1.xlsx', sheet_name='IPC')
    salario_final= calculo_nomina(salario, años_hasta_jubilacion, ipc_data)
    porcentaje_renta = min((años_trabajados // 4) * 0.0225, 0.19)
    m1 = (salario_final * porcentaje_renta)/12
    date_range = pd.date_range(start=fecha_jubilacion, periods=22*12, freq='MS')
    date_list = date_range.strftime('%Y-%m').tolist()
    intereses= []
    int1= ((1+ (interes1*0.01))**(1/12))-1
    int2= ((1+ (interes2*0.01))**(1/12))-1
    año1 = duración_interes1[0]
    mes1= duración_interes1[1]
    for i in range(0, año1*12+ mes1):
        intereses.append(int1)
    for i in range(0, (22*12) - (año1*12+ mes1)):
        intereses.append(int2)
    rentas = []
    valor =m1
    for fecha in date_list:
        mes = fecha[-2:] 
        if mes == '01':
            valor *= 1.03 
        rentas.append(valor)
    df = pd.DataFrame({'Fecha': date_list, 'Intereses': intereses, 'Pagos': rentas})
    capital_jubilacion = 0
    for i in range(len(df)-1, -1, -1):
        renta = float(df.iloc[i,2]) * (1+float(df.iloc[i,1]))**-1
        for interes in range(i, -1, -1):
            renta = renta * (1+float(df.iloc[interes,1]))**-1
        capital_jubilacion += renta
    #pasarlo a 2025
    fechas = pd.date_range(start='2025-01-01', end=fecha_jubilacion, freq='MS')
    fechas_formateadas = fechas.strftime('%Y-%m')
    
    int_ren1= ((1+ (interes_rendimiento1*0.01))**(1/12))-1
    int_ren2= ((1+ (interes_rendimiento2*0.01))**(1/12))-1
    año2= duración_interés_rendimiento1[0]
    mes2= duración_interés_rendimiento1[1]
    
    intereses1= []
    for i in range(0, año2*12+mes2):
        intereses1.append(int_ren1)
    for i in range(0, len(fechas_formateadas) - 7*12):
        intereses1.append(int_ren2)
    
    df1 = pd.DataFrame({'Fecha': fechas_formateadas, 'Intereses': intereses1})
    
    capital_actual= capital_jubilacion
    for i in range(len(df1)-1, -1, -1):
        capital_actual = capital_actual * (1+float(df1.iloc[i,1]))**-1
    
    monto_mensual = calcular_monto_mensual(capital_jubilacion, df1['Intereses'].tolist())
        
    return capital_jubilacion, capital_actual, monto_mensual


def calcular_primas_jubilacion_df(df, ipc, interes1, interes2, duracion_interes1, interes_rendimiento1, interes_rendimiento2, duracion_interes_rendimiento1):
    resultados = []
    try:
        with open("notebooks/Data Mining/modelo.pkl", "rb") as f:
            modelo = pickle.load(f)
        
        # Verificar que las columnas necesarias estén presentes
        required_columns = ['ID', 'FECHA NAC', 'SEXO', 'NOMINA BRUTA 01/01/2025', 'FECHA ENTRADA', 'PARA CONTAR MESES', 'EDAD']
        if not all(column in df.columns for column in required_columns):
            raise ValueError(f"El archivo CSV no tiene las columnas requeridas. Columnas esperadas: {required_columns}")
        
        # Preparar los datos para la predicción
        X_2 = df[['EDAD', 'NOMINA BRUTA 01/01/2025']]
        X_2.columns = ['Edad', 'Ingreso Anual (€)']
        
        # Predecir los años hasta la jubilación
        df["AÑOS HASTA JUBILACION"] = modelo.predict(X_2)
        
        # Calcular los flujos de caja para cada trabajador
        for _, row in df.iterrows():
            salario_final = calculo_nomina(row['NOMINA BRUTA 01/01/2025'], row['AÑOS HASTA JUBILACION'], ipc)
            porcentaje_renta = min((row['EDAD'] // 4) * 0.0225, 0.19)
            m1 = (salario_final * porcentaje_renta) / 12
            
            fecha_jubilacion = dt.datetime(2025, 1, 1) + dt.timedelta(days=row['AÑOS HASTA JUBILACION'] * 365)
            fecha_jubilacion = fecha_jubilacion.strftime('%Y-%m-%d')
            date_range = pd.date_range(start=fecha_jubilacion, periods=22 * 12, freq='MS')
            date_list = date_range.strftime('%Y-%m').tolist()
            
            int1 = ((1 + (interes1 * 0.01)) ** (1 / 12)) - 1
            int2 = ((1 + (interes2 * 0.01)) ** (1 / 12)) - 1
            año1, mes1 = duracion_interes1
            
            intereses = [int1] * (año1 * 12 + mes1) + [int2] * ((22 * 12) - (año1 * 12 + mes1))
            
            rentas = []
            valor = m1
            for fecha in date_list:
                if fecha[-2:] == '01':
                    valor *= 1.03
                rentas.append(valor)
            
            df_rentas = pd.DataFrame({'Fecha': date_list, 'Intereses': intereses, 'Pagos': rentas})
            
            capital_jubilacion = 0
            for i in range(len(df_rentas) - 1, -1, -1):
                renta = float(df_rentas.iloc[i, 2]) * (1 + float(df_rentas.iloc[i, 1])) ** -1
                for interes in range(i, -1, -1):
                    renta = renta * (1 + float(df_rentas.iloc[interes, 1])) ** -1
                capital_jubilacion += renta
            
            fechas = pd.date_range(start='2025-01-01', end=fecha_jubilacion, freq='MS')
            fechas_formateadas = fechas.strftime('%Y-%m')
            
            int_ren1 = ((1 + (interes_rendimiento1 * 0.01)) ** (1 / 12)) - 1
            int_ren2 = ((1 + (interes_rendimiento2 * 0.01)) ** (1 / 12)) - 1
            año2, mes2 = duracion_interes_rendimiento1
            
            intereses1 = [int_ren1] * (año2 * 12 + mes2) + [int_ren2] * (len(fechas_formateadas) - (año2 * 12 + mes2))
            df1 = pd.DataFrame({'Fecha': fechas_formateadas, 'Intereses': intereses1})
            
            capital_actual = capital_jubilacion
            for i in range(len(df1) - 1, -1, -1):
                capital_actual = capital_actual * (1 + float(df1.iloc[i, 1])) ** -1
            
            monto_mensual = calcular_monto_mensual(capital_jubilacion, df1['Intereses'].tolist())
            
            resultados.append([row['ID'], capital_jubilacion, capital_actual, monto_mensual])
        
        return pd.DataFrame(resultados, columns=['ID', 'Capital Jubilación', 'Capital Actual', 'Monto Mensual'])
    
    except Exception as e:
        print(f"Error en calcular_primas_jubilacion_df: {e}")
        raise

@app.route('/')
def index():
    return render_template('portada.html')

@app.route('/trabajador_calculadora3', methods=['GET', 'POST'])
def trabajador_calculadora3():
    if request.method == "POST":
        nombre = request.form['nombre']
        edad = int(request.form['edad_actual'])

        anos_trabajados = int(request.form['años_trabajados'])
        salario = float(request.form['salario_actual'])
        interes1 = float(request.form['interes_ahorro']) / 100
        interes2 = float(request.form['interes_renta']) / 100
        interes_rendimiento1 = float(request.form['interes_rendimiento1']) / 100
        interes_rendimiento2 = float(request.form['interes_rendimiento2']) / 100
        duracion_interes1_años = int(request.form['duracion_interes1_años'])
        duracion_interes1_meses = int(request.form['duracion_interes1_meses'])
        duracion_rendimiento1_años = int(request.form['duracion_rendimiento1_años'])
        duracion_rendimiento1_meses = int(request.form['duracion_rendimiento1_meses'])
        
        # Convertir duraciones en tuplas
        duracion_interes1 = (duracion_interes1_años, duracion_interes1_meses)
        duracion_interes_rendimiento1 = (duracion_rendimiento1_años, duracion_rendimiento1_meses)

        
        # Llamada a la función correcta (calcular_primas_jubilacion)
        resultados = calcular_primas_jubilacion(
            salario, edad, anos_trabajados, interes1, interes2, 
            duracion_interes1, interes_rendimiento1, 
            interes_rendimiento2, duracion_interes_rendimiento1
        )
        
        # Convertir resultados en un diccionario
        resultados_dict = {
            'capital_jubilacion': resultados[0],
            'capital_actual': resultados[1],
            'monto_mensual': resultados[2]
        }
        return render_template('resultado2.html', resultados=resultados_dict)
    
    return render_template('trabajador_calculadora3.html')


@app.route('/cargar_csv', methods=['GET', 'POST'])
def cargar_csv():
    resultado_csv = None
    mensaje_error = None
    
    if request.method == 'POST':
        archivo = request.files.get('archivo')  # Usamos get para evitar un KeyError
        
        # Verificar si se cargó un archivo
        if not archivo:
            mensaje_error = "No se ha cargado ningún archivo."
            return render_template('csv_calculadora.html', resultado_csv=resultado_csv, mensaje_error=mensaje_error)

        # Verificar la extensión del archivo
        if archivo.filename.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.filename.endswith('.xlsx'):
            df = pd.read_excel(archivo, engine='openpyxl')
        else:
            mensaje_error = "Formato de archivo no soportado. Solo se permiten archivos CSV y Excel."
            return render_template('csv_calculadora.html', resultado_csv=resultado_csv, mensaje_error=mensaje_error)
        
        # Verificar si el archivo tiene datos
        if df.empty:
            mensaje_error = "El archivo está vacío o no contiene datos válidos."
            return render_template('csv_calculadora.html', resultado_csv=resultado_csv, mensaje_error=mensaje_error)
        
        # Cargar datos IPC
        ipc_data = pd.read_excel('Datos/Originales/Dataset_1.xlsx', sheet_name='IPC')
        
        # Llamada a la función para calcular los resultados con el DataFrame
        try:
            resultado_csv = calcular_primas_jubilacion_df(df, ipc_data, 2, 1.5, [6, 9], 2.5, 2, [7, 0])
            resultado_csv = resultado_csv.to_html(classes="table table-striped")  # Convertir a tabla HTML
        except Exception as e:
            mensaje_error = f"Hubo un error al procesar el archivo: {str(e)}"
            return render_template('csv_calculadora.html', resultado_csv=resultado_csv, mensaje_error=mensaje_error)
    
    return render_template('csv_calculadora.html', resultado_csv=resultado_csv, mensaje_error=mensaje_error)

if __name__ == '__main__':
    app.run(debug=True)

