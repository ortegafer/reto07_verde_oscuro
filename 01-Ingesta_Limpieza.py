# INGESTA
# In: Datos originales
# Out: Datos limpios

import pandas as pd
import packages.Preprocesamiento as ppr
import os

# Load
path_datos = os.path.join('Datos','Originales')
filename = os.path.join(path_datos,'Dataset_2.csv')
df = ppr.read_data(filename)
print(df.head())

# Clean
df = ppr.remove_rows_with_nas(df, 'Age')

# Folder to save clean data
path_clean_data = os.path.join('Datos','Limpios')
if not os.path.exists(path_clean_data):
    os.makedirs(path_clean_data)

file_clean = os.path.join(path_clean_data,'datos_limpios.csv')
ppr.save_clean_data(df, file_clean)