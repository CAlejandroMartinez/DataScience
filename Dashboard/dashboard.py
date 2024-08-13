import pandas as pd
import numpy as np
import dash
from dash import dcc,html,dash_table
import plotly.express as px

df=pd.read_csv('../files/Ventas.csv')

app=dash.Dash(__name__)
categorias=[{'label':'All','value':'all'}]
for cat in np.unique(df['Categoria']):
    categorias.append({'label': cat, 'value': cat})
anios=[{'label':'All','value':'all'}]
for y in np.unique(df['Año']):
    anios.append(({'label':y,'value':y}))

app.layout= html.Div(children=[
    html.H1(children='Dashboard de Ventas'),
    html.Div(
        dcc.Dropdown(
            id='categoria',
            options=categorias,value='all')),
    html.Div(
        dcc.Dropdown(
            id='anio',
            options=anios,value='all')),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(id='grafico')
])
@app.callback(
    dash.Output('grafico','figure'),
    [dash.Input('categoria','value'),dash.Input('anio','value')]
)
def actualizar_graficoytabla(categoria_sel,anio_sel):
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
            fig = px.bar(df_filtrado, x='Semana', y='Ventas', color='Año')
            return fig
    elif anio_sel!='all':
        df_filtrado = df[df['Año'] == anio_sel]
        fig = px.bar(df_filtrado, x='Semana', y='Ventas', color='Año')
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)