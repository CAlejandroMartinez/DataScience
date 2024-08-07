''' Ejemplo de visualizacion y aplicación de Regresión lineal para estimar precios de venta de casas'''

#Librerias a utilizar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#Cargamos el archivo de entrenamiento

df=pd.read_csv('../files/train.csv')

# Definimos el estilo a utilizar en nuestras graficas
plt.style.use('tableau-colorblind10')
sns.set_style("whitegrid", {'grid.linestyle': '--'})
# Construimos una figura donde se colocaran 4 graficos , esta figura tendra una dimension de 12X12

fig, axes = plt.subplots(2,2,figsize=(12,10))
fig.subplots_adjust(hspace=0.525, wspace=0.325)
# Se contruye una matriz de correlación
corr_mat=df.corr(numeric_only=True)
# Se extraen las 10 columnas cuya correlacion con SalePrice sea la mayor
cols=corr_mat.nlargest(10,'SalePrice')['SalePrice'].index

# Se construye una matriz de correlacion unicamente con las columnas extraidas
cm = np.corrcoef(df[cols].values.T)

# Se grafica un mapa de calor, tomando como datos la matriz de correlación

sns.heatmap(ax=axes[0,0],data=cm,annot=True,fmt='.2f',yticklabels=cols.values,xticklabels=cols.values)
axes[0,0].set_title('Las 10 Principales correlaciones')
axes[0,0].tick_params(axis='x', rotation=75)
# Se muestran 3 graficas relacionando los precios con las tres columnas con mayor correlación
sns.scatterplot(ax=axes[0,1],data=df,x='GarageCars',y='SalePrice')
axes[0,1].set_title('Distribucion entre número de autos en garage y precio')
sns.scatterplot(ax=axes[1,0],data=df,x='GrLivArea',y='SalePrice')
axes[1,0].set_title('Distribucion entre longitud sotano y precio')
sns.boxplot(ax=axes[1,1],data=df,x='OverallQual',y='SalePrice')
axes[1,1].set_title('Diagrama de cajas de calidad y precio')
plt.grid()

'''Se toman las 5 columnas con mayor correlación para crear nuestro conjunto de datos'''

X=df[['OverallQual','GrLivArea','GarageCars','GarageArea','TotalBsmtSF']]
y=df['SalePrice']

# Se crea el modelo de regresión lineal
modelo=LinearRegression()

# Se crea el conjunto de entrenamiento y prueba basado  en la información seleccionada

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

# Se entrena el modelo con los datos de entrenamiento
modelo.fit(X_train,y_train)
# Se evalua el modelo
y_pred = modelo.predict(X_test)

# Calculamos y mostramos el error cuadrático medio
mse = mean_squared_error(y_test, y_pred)
print(f'Error cuadrático medio: {mse}')

# Mostramos las graficas comparando los datos de prueba y los datos estimados por el modelo
plt.figure(figsize=(10,8))
plt.plot(range(len(y_test)),y_test,c='red',label='test')
plt.plot(range(len(y_pred)),y_pred,c='blue',alpha=0.7,label='predicción')
plt.axis([0,len(y_test),0,np.max(y_pred)])
plt.title('Comparacion de datos de prueba y estimados')
plt.legend()

# Cargamos el conjunto para realizar las pruebas con el modelo desarrollado

df_test=pd.read_csv('../files/test.csv')

df_test.dropna(subset=['GarageCars','TotalBsmtSF'],inplace=True)
predicciones=modelo.predict(df_test[['OverallQual','GrLivArea','GarageCars','GarageArea','TotalBsmtSF']])
# Se muestra las estimaciones de precios de cada una de las casas del conjunto de pruebas

plt.figure(figsize=(12,8))
plt.plot(range(len(predicciones)),predicciones,c='green')
plt.axis([0,len(predicciones),0,np.max(predicciones)])
plt.title('Estimación de precios de acuerdo al modelo de regresion lineal')
# Mostramos todas las imagenes
plt.show()

