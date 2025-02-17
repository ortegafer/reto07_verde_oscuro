
def calcular_primas_jubilacion(salario_final, anios_trabajados, anios_hasta_jubilacion):
    # Parámetros
    crecimiento_renta = 0.03  # 3% de incremento anual de la renta
    tipo_interes_ahorro_1 = 0.025  # 2.5% los primeros 7 años
    tipo_interes_ahorro_2 = 0.02   # 2% después
    tipo_interes_renta_1 = 0.02    # 2% los primeros 6 años y 9 meses
    tipo_interes_renta_2 = 0.015   # 1.5% después
    duracion_renta_anios = 22
    meses_renta = duracion_renta_anios * 12
    
    # Cálculo de la renta inicial
    porcentaje_renta = min((anios_trabajados // 4) * 0.0225, 0.19)
    renta_mensual = salario_final * porcentaje_renta
    
    # Cálculo del valor actual de la renta con crecimiento del 3%
    VA = 0
    umbral = 6 * 12 + 9  # 81 meses
    
    for t in range(1, meses_renta + 1):
        # Calcular el pago mensual con crecimiento anual
        R_t = renta_mensual * (1 + crecimiento_renta) ** (t // 12)
        
        if t < umbral:
            # Factor de descuento para t menor a umbral
            DF = (1 + tipo_interes_renta_1/12) ** t
        else:
            # Para t >= umbral: descontamos hasta el umbral con la tasa 1
            # y el resto con la tasa 2
            DF = (1 + tipo_interes_renta_1/12) ** umbral * (1 + tipo_interes_renta_2/12) ** (t - umbral)
        
        VA += R_t / DF

    
    # Crecimiento del ahorro hasta la jubilación
    if anios_hasta_jubilacion <= 7:
        VA_en_hoy = VA / ((1 + tipo_interes_ahorro_1) ** anios_hasta_jubilacion)
    else:
        VA_en_hoy = VA / ((1 + tipo_interes_ahorro_1) ** 7 * (1 + tipo_interes_ahorro_2) ** (anios_hasta_jubilacion - 7))
    
    
    # Cálculo de la prima mensual (ajustado para el rendimiento de las inversiones)
    n = anios_hasta_jubilacion * 12  # Número total de meses

    # Cálculo del valor presente de los primeros 7 años
    n_1 = min(7 * 12, n)  # Número de meses hasta 7 años
    i_mensual_1 = tipo_interes_ahorro_1 / 12
    VA_1 = VA_en_hoy * (i_mensual_1) / ((1 + i_mensual_1) ** n_1 - 1) if n_1 > 0 else 0

    # Cálculo del valor presente de los años después de 7 años
    n_2 = max(n - 7 * 12, 0)  # Número de meses después de los 7 primeros años
    i_mensual_2 = tipo_interes_ahorro_2 / 12
    VA_2 = VA_en_hoy * (i_mensual_2) / ((1 + i_mensual_2) ** n_2 - 1) if n_2 > 0 else 0

    # La prima mensual es la suma de ambos valores presentes
    prima_mensual = VA_1 + VA_2
    prima_unica_2025 = VA_en_hoy
    prima_unica_jubilacion = VA
    
    return {
        "VA en la jubilación": VA,
        "VA hoy": VA_en_hoy,
        "Prima mensual": prima_mensual,
        "Prima única en 2025": prima_unica_2025,
        "Prima única en la jubilación": prima_unica_jubilacion
    }

# Ejemplo de uso
salario_final = 3  # Última nómina del empleado
anios_trabajados = 34  # Años en la empresa
anios_hasta_jubilacion = 13  # Años restantes hasta la jubilación

resultado = calcular_primas_jubilacion(salario_final, anios_trabajados, anios_hasta_jubilacion)
print(resultado)
