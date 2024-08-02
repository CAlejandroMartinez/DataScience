'''Este ejemplo hace uso de un archivo sql para reconstruir las tablas de una base de datos, posteriormente se aplica
un analisis exploratorio y se completan los datos faltantes, finalmente, se procede a almacenar las tablas, esto puede ser
dentro de un archivo sql, xlsx o csv, en el ejemplo se guadar en archivos CSV'''

import pandas as pd
import sqlite3

conn= sqlite3.connect(':memory:')
conn.text_factory = lambda data: str(data, encoding="latin1")
with conn as connection:
    # Leer el archivo SQL
    with open('../files/mysqlsampledatabase.sql', 'r') as file:
        sql_script = file.read()

sql_script=sql_script.replace('CREATE DATABASE','/*',1)
sql_script=sql_script.replace('USE ','/* ',1)
sql_script=sql_script.replace("\\'","")
conn.executescript(str(sql_script))

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
nombres = cursor.fetchall()
tabla_nombres=[]
for n in range(len(nombres)):
    tabla_nombres.append(nombres[n][0])
df_tablas={}

for names in tabla_nombres:
    df_tablas[names]=pd.read_sql(f'SELECT * FROM {names}',conn)

print('*'*75)
#Análisis de datos exploratorio para cada tabla
for names in tabla_nombres:
    print(f'Resumen estadístico de {names}')
    print(df_tablas[names].info())
    print(df_tablas[names].describe())
    print('*'*75)

#Tatamiendo de datos ausentes para cada tabla
'''Tabla productlines los datos ausentes son rellenados con la palabra unknow '''

df_tablas['productlines'].fillna('unknow',inplace=True)
print(df_tablas['productlines'].info())

'''Tabla offices, la columna 'state' podria completarse utilizando el 'postalCode' , sin embargo no queremos extendernos
en este ejemplo '''
df_tablas['offices'].fillna('uknow',inplace=True)
print(df_tablas['offices'].info())

'''Tabla employees la columna reportsTo debe ser convertido el tipo de dato de float a int y el dato faltante se colocará como 0,
la columna officeCode tambien se cambia a int'''

df_tablas['employees'].fillna(0,inplace=True)
df_tablas['employees']=df_tablas['employees'].astype({'reportsTo':'int64','officeCode':'int32'})
print(df_tablas['employees'].info())


''' La tabla customers- La columna adressLine2 es llenada con la palabra unknow, la columna state podría ser llenada utilizando el
 postalCode pero no es el motivo de este ejemplo por que se llenará como unknow, de igual manera con los datos faltantes de la 
  columna postalCode, la cual se modificará de tipo de dato a int32 y los datos  ausentes se cambiaran a cero. Finalmente la columna 
  salesRepEmployer, los datos faltantes serán llenados con cero y posteriormente el tipo de dato de la columna se modificará a int64 '''

df_tablas['customers'].fillna({'addressLine2':'unknow','state':'unknow','postalCode':'unknow','salesRepEmployeeNumber':0}, inplace=True)
df_tablas['customers']=df_tablas['customers'].astype({'salesRepEmployeeNumber':'int64'})
print(df_tablas['customers'].info())

''' La tabla orders- Tiene datos incompletos em shippedDate y comments, adicional las columnas orderDate, requiredDate y shippedDate
  tiene que convertirse a formato fecha. La columna shippedDate podría llenarse a partir de una interpolacíon en el supuesto que las
  el numero de orden indica el orden en que fueron ordenadas, requeridas y vendidas, como no es el objetivo de este ejemplo se 
  eliminaran los 10 registros con informacion incompleta'''

df_tablas['orders']['orderDate']=pd.to_datetime(df_tablas['orders']['orderDate'],format='%Y-%m-%d')
df_tablas['orders']['requiredDate']=pd.to_datetime(df_tablas['orders']['requiredDate'],format='%Y-%m-%d')
df_tablas['orders']['shippedDate']=pd.to_datetime(df_tablas['orders']['shippedDate'],format='%Y-%m-%d')
df_tablas['orders'].fillna({'comments':'none'},inplace=True)
df_tablas['orders']=df_tablas['orders'].dropna()
print(df_tablas['orders'].info())

for names in tabla_nombres:
        df_tablas[names].to_csv(names+'.csv',index=False)