# INGESTA
# In: Datos originales
# Out: Datos limpios
import pandas as pd
import packages.Preprocesamiento as ppr
import os
import datetime as dt
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

#Load dataset 1
path_datos = os.path.join('Datos','Originales')
filename = os.path.join(path_datos,'Dataset_1.xlsx')
df = pd.read_excel(filename, skiprows=2, header=1)
print(df.head())

print(df.describe()) #no parece que haya outliers

print(df.info()) #formato adecuado

print(df.isna().sum()) #no hay NAs

print(df.duplicated().unique()) #no hay duplicados

today = pd.Timestamp.now()
df['EDAD'] = df['FECHA NAC'].apply(lambda x: today.year - x.year) 
#tenemos en cuenta solo el año, para que todos los nacidos en el mismo año tengan la misma edad

#Load dataset 2
path_datos = os.path.join('Datos','Originales')
filename = os.path.join(path_datos,'Dataset_2.csv')
df2 = pd.read_csv(filename)
print(df2.head())

print(df2.describe())

print(df2.info()) #formato adecuado

print(df2.isna().sum()) #no hay NAs

print(df2.duplicated().unique()) #no hay duplicados

#datos1_limpios.csv
path_clean_data = os.path.join('Datos','Limpios')
if not os.path.exists(path_clean_data):
    os.makedirs(path_clean_data)

file_clean = os.path.join(path_clean_data,'datos1_limpios.csv')
ppr.save_clean_data(df, file_clean)

#datos2_limpios.csv
path_clean_data = os.path.join('Datos','Limpios')
if not os.path.exists(path_clean_data):
    os.makedirs(path_clean_data)

file_clean = os.path.join(path_clean_data,'datos2_limpios.csv')
ppr.save_clean_data(df2, file_clean)