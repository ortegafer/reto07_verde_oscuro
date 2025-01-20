import pandas as pd

def read_data(filename):
    """
    Lee un archivo CSV y devuelve un DataFrame.

    Args:
        filename (str): Ruta del archivo CSV a leer.

    Returns:
        pd.DataFrame: DataFrame con los datos del archivo.
    """
    return pd.read_csv(filename)

def read_data2(filename):
    """
    Lee un archivo CSV y devuelve un DataFrame, con la primera columna como índice.

    Args:
        filename (str): Ruta del archivo CSV a leer.

    Returns:
        pd.DataFrame: DataFrame con los datos del archivo, usando la primera columna como índice.
    """
    return pd.read_csv(filename, index_col=0)

def remove_column(df, colnames):
    """
    Elimina las columnas especificadas de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        colnames (str o list): Nombre o lista de nombres de columnas a eliminar.

    Returns:
        pd.DataFrame: DataFrame sin las columnas especificadas.
    """
    return df.drop(columns=colnames)

def remove_rows_with_nas(df, colnames):
    """
    Elimina las filas que tienen valores nulos en las columnas especificadas.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        colnames (str): Nombre de la columna que se revisará para valores nulos.

    Returns:
        pd.DataFrame: DataFrame sin las filas con valores nulos en las columnas especificadas.
    """
    return df[df[colnames].notna()]

def save_clean_data(df, file):
    """
    Guarda un DataFrame limpio en un archivo CSV.

    Args:
        df (pd.DataFrame): DataFrame a guardar.
        file (str): Ruta del archivo donde se guardarán los datos.

    Returns:
        None: La función no devuelve nada, solo guarda el archivo.
    """
    df.to_csv(file)
    return None

def cambio_hora(df, colname):
    """
    Convierte una columna de un DataFrame a tipo datetime.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        colname (str): Nombre de la columna que se convertirá a datetime.

    Returns:
        pd.DataFrame: DataFrame con la columna convertida a datetime.
    """
    df[colname] = pd.to_datetime(df[colname], errors='coerce')
    return df

def cambiar_tipo_columnas(df, columna, nuevo_tipo):
    """
    Cambia el tipo de una columna específica en un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        columna (str): Nombre de la columna que cambiará de tipo.
        nuevo_tipo (str): El nuevo tipo de la columna (por ejemplo, 'int', 'float', etc.).

    Returns:
        pd.DataFrame: DataFrame con la columna convertida al nuevo tipo.
    """
    try:
        df[columna] = df[columna].astype(nuevo_tipo)
    except ValueError as e:
        print(f"Error al convertir la columna '{columna}' a {nuevo_tipo}: {e}")
    except KeyError:
        print(f"La columna '{columna}' no existe en el DataFrame.")
    return df

def eliminar_duplicados(df, subset=None, keep="first"):
    """
    Elimina filas duplicadas en un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        subset (str o list, opcional): Columna(s) para identificar duplicados. Si es None, se considera todas las columnas.
        keep (str, opcional): Qué duplicado conservar. Puede ser 'first', 'last' o False (eliminar todos).

    Returns:
        pd.DataFrame: DataFrame sin duplicados.
    """
    df = df.drop_duplicates(subset=subset, keep=keep)
    return df

def cambio_comas(df, columname):
    """
    Reemplaza las comas por puntos en una columna de texto de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de entrada.
        columname (str): Nombre de la columna en la que se reemplazarán las comas.

    Returns:
        pd.DataFrame: DataFrame con las comas reemplazadas por puntos en la columna especificada.
    """
    df[columname] = df[columname].str.replace(',', '.')
    return df

def map_columnas(df, column_name, mapping_dict):
    """
    Aplica un mapeo a una columna específica de un DataFrame.

    Args:
        df (pd.DataFrame): DataFrame al que se le aplicará el mapeo.
        column_name (str): Nombre de la columna a transformar.
        mapping_dict (dict): Diccionario de mapeo que define la transformación.

    Returns:
        pd.DataFrame: DataFrame con la columna transformada.
    """
    if column_name in df.columns:
        df[column_name] = df[column_name].map(mapping_dict)
    else:
        raise KeyError(f"La columna '{column_name}' no existe en el DataFrame.")
    return df
