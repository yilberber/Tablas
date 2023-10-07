from dash import Dash, dash_table, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.tools as tls
import plotly.graph_objs as go
from backend.granulometria import granulometria

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def generate_granulometria_plot():
    trace = go.Scatter(
        x=granulometria['Abertura'][0:11],
        y=granulometria['Por_Pasa'][0:11],
        mode='lines',
        line=dict(color='black', width=2),
        name='Curva Granulométrica'
    )
    
    layout = go.Layout(
        title='Curva Granulométrica',
        xaxis=dict(
            title='Tamiz (mm)',
            type='log',
            autorange=True
        ),
        yaxis=dict(
            title='Porcentaje Pasa Acumulado %',
            range=[0, 100]
        )
    )

    return {'data': [trace], 'layout': layout}


#App layout
app.layout = dbc.Container(
    [
        html.H1("Realización de tablas"),
        dash_table.DataTable(
            id='tabla_granulometria',
            columns=[
                {'name': 'Malla', 'id': 'Malla','editable': False},
                {'name': 'Abertura', 'id': 'Abertura','editable': False},
                {'name': 'Retenido', 'id': 'Retenido', 'editable': True},
                {'name': 'Retenido_acum', 'id': 'Retenido_acum', 'editable': False},
                {'name': 'Pasa', 'id': 'Pasa', 'editable': False},
                {'name': 'Por_Pasa', 'id': 'Por_Pasa', 'editable': False}
            ],
            data=granulometria.to_dict('records')           
            ),
        dcc.Graph(id='granulometria-plot')
        
        
        
    ],
    fluid=True
)

@app.callback(
    Output('tabla_granulometria', 'data'),
    [Input('tabla_granulometria', 'data'),
     Input('tabla_granulometria', 'columns')]
)

def update_granulometria_table(rows, columns):
    granulometria = pd.DataFrame(rows)
    granulometria["Retenido"] = granulometria["Retenido"].astype("int") 
    granulometria["Retenido_acum"]= granulometria["Retenido"].cumsum() #se crea una columna para retenido acummulado y se aplica cumsum a la columna retenido para hallar su acumulado
    granulometria["Pasa"]= granulometria["Retenido"].sum()-granulometria["Retenido_acum"] #Se crea la columna Pasa y se realiza la resta del total de la muestra menos el retenido acumulado en cada fila
    granulometria["Por_Pasa"]= round(granulometria["Pasa"]*100/granulometria["Retenido"].sum(),2) #Se crea la columna % pasa y se realiza la operació entre la columna pasa por 100 dividido en el total de la muetra
      
    # Convertir las columnas numéricas a str para evitar el error
    granulometria["Retenido"] = granulometria["Retenido"].astype(str)
    granulometria["Retenido_acum"] = granulometria["Retenido_acum"].astype(str)
    granulometria["Pasa"] = granulometria["Pasa"].astype(str)
    granulometria["Por_Pasa"] = granulometria["Por_Pasa"].astype(str)
         
    return granulometria.to_dict('records')

@app.callback(
    Output('granulometria-plot', 'figure'),
    [Input('tabla_granulometria', 'data')]
)
def update_granulometria_plot(rows):
    granulometria = pd.DataFrame(rows)
    
    trace = go.Scatter(
        x=granulometria['Abertura'][0:11],
        y=granulometria['Por_Pasa'][0:11],
        mode='lines',
        line=dict(color='black', width=2),
        name='Curva Granulométrica'
    )
    
    layout = go.Layout(
        title='Curva Granulométrica',
        xaxis=dict(
            title='Tamiz (mm)',
            type='log',
            autorange=True
        ),
        yaxis=dict(
            title='Porcentaje Pasa Acumulado %',
            range=[0, 100]
        )
    )

    return {'data': [trace], 'layout': layout}

if __name__ == "__main__":
    app.run_server(debug=True)