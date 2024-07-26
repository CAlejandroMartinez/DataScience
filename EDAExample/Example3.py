'''En este ejemplo se realiza un cambio al tipo de datos, utilizando una función para retirar
strings los cuales no permiten la transformación directa
'''

#Se importa la libreria pandas, la cual permite leer archivos CSV, xlsx y sql

import pandas as pd
import chardet
import re
# Se define la dirección donde se encuentra el documento

url='../files/LondonBikeJourneyAug2023.csv'

# Verificamos si el archivo tiene alguna codificación especial

with open(url, 'rb') as file:
    data = file.read(100000)
    result = chardet.detect(data)
    encode=result['encoding']
    print(f"El archivo  esta codificado como: {result['encoding']}")

# se crea un data frame apartir de la lectura del archivo csv con la codificación específica
df = pd.read_csv(url,encoding=encode)

# Se define la función encargada de eliminar y transformar los datos al formato de tiempo correcto
# Función para convertir el tiempo
def convertir_a_hms(duration):
    # Extrae días, horas, minutos y segundos
    dias = int(re.search(r'(\d+)d', duration).group(1)) if 'd' in duration else 0
    horas = int(re.search(r'(\d+)h', duration).group(1)) if 'h' in duration else 0
    minutos = int(re.search(r'(\d+)m', duration).group(1)) if 'm' in duration else 0
    segundos = int(re.search(r'(\d+)s', duration).group(1)) if 's' in duration else 0

    # Convierte todo a segundos y luego a h:m:s
    total_segundos = dias * 86400 + horas * 3600 + minutos * 60 + segundos
    final_horas= total_segundos // 3600
    final_minutos = (total_segundos % 3600) // 60
    final_segundos = total_segundos % 60

    return f'{final_horas:02}:{final_minutos:02}:{final_segundos:02}'


# Se aplica la función para convertir los datos
df['Total duration'] = df['Total duration'].apply(convertir_a_hms)

print(df['Total duration'])