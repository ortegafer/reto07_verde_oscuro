def calculo_nomina(salario_actual, años_hasta_jubilación):
    import math
    import pandas as pd
    redondeado = math.floor(años_hasta_jubilación)
    salario = salario_actual
    ipc= pd.read_excel('Datos/Originales/Dataset_1.xlsx', sheet_name='IPC')
    for i in range(0, redondeado):
        salario = salario + salario*ipc.iloc[i,1]
    return float(salario)

def calcular_primas_jubilacion(salario, años_trabajados, años_hasta_jubilacion, fecha_jubilación):
    salario_final= calculo_nomina(salario, años_hasta_jubilacion)
    porcentaje_renta = min((años_trabajados // 4) * 0.0225, 0.19)
    m1 = (salario_final * porcentaje_renta)/12
    import datetime as dt
    import pandas as pd
    date_range = pd.date_range(start=fecha_jubilación, periods=22*12, freq='MS')
    date_list = date_range.strftime('%Y-%m').tolist()
    intereses= []
    for i in range(0, 6*12+9):
        intereses.append(0.00165)
    for i in range(0, (22*12) - (6*12+9)):
        intereses.append(0.00124)
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
    fechas = pd.date_range(start='2025-01-01', end=fecha_jubilación, freq='MS')
    fechas_formateadas = fechas.strftime('%Y-%m')
    
    intereses1= []
    for i in range(0, 7*12):
        intereses1.append(0.00165)
    for i in range(0, len(fechas_formateadas) - 7*12):
        intereses1.append(0.00205)
    
    df1 = pd.DataFrame({'Fecha': fechas_formateadas, 'Intereses': intereses1})
    
    capital_actual= capital_jubilacion
    for i in range(len(df1)-1, -1, -1):
        capital_actual = capital_actual * (1+float(df1.iloc[i,1]))**-1
    
    capital_actual

    return capital_jubilacion, capital_actual

print(calcular_primas_jubilacion(15319.07,36,13.55, '2038-11-20'))