'''En este ejemplo se realiza un analisis exploratprop básico:
- Se carga un archivo CSV
- Se revisan las dimensiones del documento
- Se muestran los primeros 5 registros
- Se muestran los ultimos 5 registros
- Se muestra un resumen estadistico del contenido del data frame
- Se muestra los tipos de datos y si alguno es nullo
- Se muestra la suma de registros nulos por columna en caso de existir  '''

#Se importa la libreria pandas, la cual permite leer archivos CSV, xlsx y sql

import pandas as pd

# Se define la direccion donde se encuentra el documento

url='../files/LondonBikeJourneyAug2023.csv'

# se crea un data frame apartir de la lectura del archivo csv
df = pd.read_csv(url)

# Mostramos las dimensiones del documento
print(f'El data frame esta compuesto por {df.shape[1]} columnas y {df.shape[0]} filas')
# Mostramos el tipo de datos en el data frame

print(df.info())

# En este caso notaremos  que existen datos tipos object por lo cual debemos visualizar algunos registros

print(df.head(5))

# Estos registros indican que los tipo object se refieren a fechas y horas por lo cual es necesario cambiar este tipo de datos

