# FUNCIÓN QUE CALCULA LOS 3 FLUJOS DE CAJA PARA TODOS LOS TRABAJADORES
# In: Datos trabajadores y Datos IPC
# Out: 3 flujos de caja para cada trabajador
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
    sum=0
    for i in range(len(intereses)):
        num= 1
        for j in range(0, len(intereses[:i+1])):
            num*=(1+intereses[j])**(-1)
        sum+= num
    
    monto = capital/sum
    return monto

def calcular_primas_jubilacion_df(df, ipc, interes1, interes2, duracion_interes1, interes_rendimiento1, interes_rendimiento2, duracion_interes_rendimiento1):
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

# Cargar los datos y calcular resultados
df_input = pd.read_csv('Datos/Limpios/datos1_limpios.csv', index_col=0)
ipc_data = pd.read_excel('Datos/Originales/Dataset_1.xlsx', sheet_name='IPC')
resultados_df = calcular_primas_jubilacion_df(df_input, ipc_data, 2, 1.5, [6,9], 2.5, 2, [7,0])
print(resultados_df)
