import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

#importamos el archivo de departamentos
departamentos = gpd.read_file('data/Departamentos.zip')

#importamos el archivo de DrenajeDoble
rios = gpd.read_file('data/DrenajeDoble.zip')

#importamos el archivo de colegios
colegios = gpd.read_file('data/EstablecimientosEducativos.zip')

def consultarDepartamento(departamento_consultado):

    #hacemos consulta del departamento buscado
    departamento_buscado = departamentos.query(f"DeNombre == '{departamento_consultado}'")
    #hacemos la intersección
    rios_departamento_buscado = gpd.overlay(departamento_buscado , rios, how='intersection')
    #hacemos busqueda colegio por departamento buscado
    colegios_departamento_buscado = colegios.query(f"DeNombre == '{departamento_consultado.upper()}'")
        

    #hacemos un buffer de los rios
    rios_departamento_buscado["buffer"] = rios_departamento_buscado.buffer(500)

    #hacemos otra intersección
    colegios_afectados = gpd.overlay(
        colegios_departamento_buscado,
        rios_departamento_buscado.set_geometry("buffer"),
        how='intersection')

    rios_departamento_buscado_4326 = rios_departamento_buscado.to_crs(epsg=4326)
    rios_departamento_buscado_4326['buffer'] = rios_departamento_buscado_4326['buffer'].to_crs(epsg=4326)
    colegios_afectados_4326 = colegios_afectados.to_crs(epsg=4326)


    # Genera mapa de ríos
    fig = px.choropleth_mapbox(
        geojson=rios_departamento_buscado_4326['buffer'].geometry,
        locations=rios_departamento_buscado_4326.index
    )

    # Agregar colegios al mapa
    fig.add_trace(
        go.Scattermapbox(
            lat=colegios_afectados_4326.geometry.y,
            lon=colegios_afectados_4326.geometry.x,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9,
                color='red'
            ),
            text=colegios_afectados_4326['Nombre'],
            hoverinfo='text'
        )
    )

    # agregamos el mapa
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=5,
        mapbox_center = {"lat": 4.6, "lon": -74},
    )
    
    return fig

