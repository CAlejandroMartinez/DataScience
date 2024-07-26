'''En este ejemplo se realiza un analisis exploratprop básico:
- Se verifica el tipo de enconding del archivo csv
- Se carga el archivo CSV y se utiliza su respectivo encoding
- Se modifica el tipo de dato Object a un formato fecha adecuado
- Se muestra el resumen estadistico del data frame
'''

#Se importa la libreria pandas, la cual permite leer archivos CSV, xlsx y sql

import pandas as pd
import chardet

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

# Mostramos las dimensiones del documento

print(f'El data frame esta compuesto por {df.shape[1]} columnas y {df.shape[0]} filas')

# Mostramos los tipos de datos en el data frame

print(df.info())

# En este caso notaremos  que existen datos de tipo object por lo cual debemos visualizar algunos registros

print(df.head(3))

'''Estos registros indican que algunos tipo object se refieren a fechas y horas por lo cual es necesario cambiar este tipo de datos
notese que no todos los tipo object corresponden a fechas, ejemplo 'Start station' 'End station' se refieren a nombres de estaciones
'''
df['Start date']=pd.to_datetime(df['Start date'],format='%d/%m/%Y %H:%M')
df['End date']=pd.to_datetime(df['End date'],format='%d/%m/%Y %H:%M')

# Mostramos el tipo de datos en el data frame con los cambios

print('*'*50)
print('Después de hacer correcciones en el tipo de dato')
print(df.info())
# Mostrando el resumen estadistico. Los objetos de tipo object son excluidos del calculo
print(df.describe())

'''En el caso de la columna Total duration es necesario realizar algunas adecuaciones al formato del contenido
lo cual se explica en el Example3 '''