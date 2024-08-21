''' En este ejemplo se realiza la combinacion de diferentes tablas utilizando las opciones:
-Merge
-Join
-Concatenate
-Compare
se utlizan las tablas relacionales del ejemplo de SQL '''

# importamos las librerias que se utilizarán

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.gridspec as gridspec

# Cargamos las tablas a utilizar

customers = pd.read_csv('../files/customers.csv')
employees = pd.read_csv('../files/employees.csv')
offices = pd.read_csv('../files/offices.csv')
orderDetails = pd.read_csv('../files/orderdetails.csv')
orders = pd.read_csv('../files/orders.csv')
payments = pd.read_csv('../files/payments.csv')
productLines = pd.read_csv('../files/productlines.csv')
products = pd.read_csv('../files/products.csv')

# Mostramos algunas graficas de nuestro interés

df_empleados_vendedores=employees.merge(customers,how='inner',left_on='employeeNumber',right_on='salesRepEmployeeNumber')
fig = plt.figure(figsize=(12,7))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2])
sns.color_palette("bright")
sns.set_context("talk")
ax3 = fig.add_subplot(gs[1, :])
sns.histplot(data=df_empleados_vendedores,x='lastName',discrete=True,shrink=.9,ax=ax3,hue='lastName',legend=False)
ax3.set_xlabel('Vendedores')
ax3.set_ylabel('Numero de clientes')
ax3.set_title('Clientes por vendedor')
plt.xticks(fontsize=9)

df_pais_vendedor = offices.merge(df_empleados_vendedores,how='inner',left_on='officeCode',right_on='officeCode')
ax1= fig.add_subplot(gs[0,0])
sns.histplot(data=df_pais_vendedor,x='country_x',ax=ax1,hue='country_x',legend=False)
ax1.set_title('Clientes por pais')

ax2 = fig.add_subplot(gs[0,1])
sns.histplot(data= orders, x='status',ax=ax2,hue='status',legend=False)
plt.yscale('log')
ax2.set_title('Estatus de ordenes')
plt.tight_layout()

df_productos_vendidos=orderDetails.merge(products,how='inner',left_on='productCode',right_on='productCode')
df_ordenes_pagadas = orders.merge(payments, how='inner',left_on='customerNumber',right_on='customerNumber')
df_ventas= df_productos_vendidos.merge(df_ordenes_pagadas,how='inner',left_on='orderNumber',right_on='orderNumber')
print(df_ventas.info())


fig2=plt.figure(figsize=(10,8))
ax1=fig2.add_subplot(1,1,1)
sns.histplot(df_ventas,x='productLine',hue='status',discrete=True,shrink=0.8 ,ax=ax1)
plt.xticks(fontsize=9)
ax1.set_title('Numero de ventas por linea de productos')

fig3=plt.figure(figsize=(8,8))
ventas_lineaProd= df_ventas.groupby('productLine')['amount'].sum()
plt.pie(ventas_lineaProd,labels=ventas_lineaProd.index, autopct='%1.1f%%', startangle=140)


df_ventas['paymentDate']=pd.to_datetime(df_ventas['paymentDate'],format='%Y-%m-%d')
df_ventas['mes']=df_ventas['paymentDate'].dt.month
df_ventas['anio']=df_ventas['paymentDate'].dt.year
ventas_x_mes=df_ventas.groupby([df_ventas['anio'],df_ventas['mes']])['amount'].sum()
df_resultado = ventas_x_mes.reset_index()
df_resultado.columns = ['año', 'mes', 'ventas_T']
df_resultado['crecimiento']=df_resultado['ventas_T'].pct_change()
print(df_resultado.info())
fig4=plt.figure(figsize=(12,8))
gs1=gridspec.GridSpec(2,1)
ax4= fig4.add_subplot(gs1[0])
ax5=fig4.add_subplot(gs1[1])
df_resultado['año']=df_resultado['año'].astype(str)
sns.barplot(df_resultado,x='mes',y='ventas_T',hue='año',ax=ax4,palette="Set2")
sns.lineplot(df_resultado,x='mes',y='crecimiento',hue='año', markers='x',ax=ax5,palette="Set2")
plt.tight_layout()
plt.show()

