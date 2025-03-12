import pandas as pd
import pickle
import math
import datetime as dt

def calculo_nomina(salario_actual, años_hasta_jubilación, ipc):
    redondeado = math.floor(años_hasta_jubilación)
    salario = salario_actual
    for i in range(0, redondeado):
        salario = salario + salario * ipc.iloc[i, 1]
    return float(salario)

def calcular_monto_mensual(capital, intereses):
    n_periodos = len(intereses)
    sumatorio = sum((1 + intereses[i]) ** (i + 1) for i in range(n_periodos))
    return capital / sumatorio

def calcular_primas_jubilacion_df(df, ipc, lista_intereses):
    resultados = []
    with open("notebooks/Data Mining/modelo.pkl", "rb") as f:
        modelo = pickle.load(f)
    X_2 = df.drop(['ID', 'FECHA NAC', 'SEXO', 'FECHA ENTRADA', 'PARA CONTAR MESES'], axis=1)
    X_2.columns = ['Ingreso Anual (€)','Edad']
    X_2 = X_2[['Edad','Ingreso Anual (€)']]
    df["AÑOS HASTA JUBILACION"] = modelo.predict(X_2)
    for _, row in df.iterrows():
        salario_final = calculo_nomina(row['NOMINA BRUTA 01/01/2025'], row['AÑOS HASTA JUBILACION'], ipc)
        porcentaje_renta = min((row['EDAD'] // 4) * 0.0225, 0.19)
        m1 = (salario_final * porcentaje_renta) / 12
        
        fecha_jubilacion = dt.datetime(2025, 1, 1) + dt.timedelta(days=row['AÑOS HASTA JUBILACION'] * 365)
        fecha_jubilacion = fecha_jubilacion.strftime('%Y-%m-%d')
        date_range = pd.date_range(start=fecha_jubilacion, periods=22 * 12, freq='MS')
        date_list = date_range.strftime('%Y-%m').tolist()
        
        if len(lista_intereses) < len(date_list):
            raise ValueError(f"La lista de intereses es demasiado corta. Se requieren {len(date_list)} valores, pero solo se proporcionaron {len(lista_intereses)}.")
        
        intereses = lista_intereses[:len(date_list)]
        
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
        
        if len(lista_intereses) < len(fechas_formateadas):
            raise ValueError(f"La lista de intereses es demasiado corta. Se requieren {len(fechas_formateadas)} valores, pero solo se proporcionaron {len(lista_intereses)}.")
        
        intereses1 = lista_intereses[:len(fechas_formateadas)]
        df1 = pd.DataFrame({'Fecha': fechas_formateadas, 'Intereses': intereses1})
        
        capital_actual = capital_jubilacion
        for i in range(len(df1) - 1, -1, -1):
            capital_actual = capital_actual * (1 + float(df1.iloc[i, 1])) ** -1
        
        monto_mensual = calcular_monto_mensual(capital_jubilacion, df1['Intereses'].tolist())
        
        resultados.append([row['ID'], capital_jubilacion, capital_actual, monto_mensual])
    
    return pd.DataFrame(resultados, columns=['ID', 'Capital Jubilación', 'Capital Actual', 'Monto Mensual'])