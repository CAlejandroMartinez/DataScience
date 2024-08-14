'''En este ejemplo se desarrolla un dashboard simple en el cual se pueden filtrar categorias y años para visualizar
las ventas realizadas por semana, con ayuda de la libreria plotly es posible visualizar la información en cada uno de
los componentes de la gráfica'''

#Librerias que serán utilizadas
import pandas as pd
import numpy as np
import dash
from dash import dcc,html,dash_table
import plotly.express as px

# lectura del archivo csv a utilizar

df=pd.read_csv('../files/Ventas.csv')

# Se crea el tablero

app=dash.Dash(__name__)

# creamos los arreglos categorias y anios para cargar dos listas desplegables

categorias=[{'label':'All','value':'all'}]
for cat in np.unique(df['Categoria']):
    categorias.append({'label': cat, 'value': cat})
anios=[{'label':'All','value':'all'}]
for y in np.unique(df['Año']):
    anios.append(({'label':y,'value':y}))

# Creamos el layout donde se mostraran dos listas deplegables, una tabla para mostrar la informacion del dataframe
# Se crea la seccion donde se mostrará el grafico de acuerdo a las elecciones de las listas desplegables

app.layout= html.Div(children=[
    html.H1(children='Dashboard de Ventas'),
    html.Div(
        dcc.Dropdown(
            id='categoria',
            options=categorias,value='all'

        )),
    html.Div(
        dcc.Dropdown(
            id='anio',
            options=anios,value='all')),
    dash_table.DataTable(id='tabla',data=df.to_dict('records'), page_size=10),
    dcc.Graph(id='grafico')
])

# Callback para actualizar el grafico despues de una seleccion en las listas desplegables
@app.callback(
    dash.Output('grafico','figure'),
    [dash.Input('categoria','value'),dash.Input('anio','value')]
)
def actualizar_grafico(categoria_sel,anio_sel):
    if categoria_sel=='all' and anio_sel=='all':
        fig=px.bar(df,x='Semana',y='Ventas',color='Año')
        return fig
    elif categoria_sel!='all':
        if anio_sel=='all':
            df_filtrado = df[df['Categoria'] == categoria_sel]
            fig = px.bar(df_filtrado, x='Semana', y='Ventas', color='Año')
            return fig
        else:
            df_prefiltrado = df[df['Categoria'] == categoria_sel]
            df_filtrado=df_prefiltrado[df_prefiltrado['Año']==anio_sel]
            fig = px.bar(df_filtrado, x='Semana', y='Ventas', color='Categoria')
            return fig
    elif anio_sel!='all':
        df_filtrado = df[df['Año'] == anio_sel]
        fig = px.bar(df_filtrado, x='Semana', y='Ventas', color='Categoria')
        return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)