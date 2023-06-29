from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import json

def generate_geo_graph(df, app):
    # Lendo o GeoJson do Brasil
    geojson = json.load(open('./dados/geojson/brasil_estados.json'))

    button_group = html.Div([
        dbc.RadioItems(
            id="casos-radio",
            class_name="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {'label': 'Cura', 'value': 1},
                {'label': 'Óbito SRAG', 'value': 2},
                {'label': 'Óbito por outras causas', 'value': 3}
            ],
            value=2,
        )],
        className="radio-group",
    )

    htmlGeo = dbc.Col(
        [
            html.Div([
                html.H4(children='Casos por Estados', style={'textAlign': 'center'}),
                button_group,
                dcc.Graph(id="geo-bar-graph"),
                dcc.Graph(id="geo-graph"),
            ])
        ]
    )

    @app.callback(
        Output('geo-bar-graph', 'figure'),
        Output('geo-graph', 'figure'),
        Input('casos-radio', 'value')
    )
    def update_geo_graph(evolucao_selecionada):
        casos = df[['UF', 'EVOLUCAO_CASO']].query('EVOLUCAO_CASO == ' + str(evolucao_selecionada)).groupby('UF').sum().reset_index()

        fig_bar = px.bar(casos, y='EVOLUCAO_CASO', x='UF',text='EVOLUCAO_CASO',
             color='EVOLUCAO_CASO',color_continuous_scale = 'Reds')          

        fig_bar.update_traces(texttemplate='%{text:.2s %}', textposition='outside')
        fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig_bar.update_layout(xaxis={'categoryorder':'total ascending'})

        fig_choropleth = px.choropleth(casos, geojson=geojson, locations='UF', color='EVOLUCAO_CASO',
                           color_continuous_scale="Reds",
                           range_color=(3000, 99999),
                            scope='south america'
                          )


        return fig_bar, fig_choropleth

    return htmlGeo