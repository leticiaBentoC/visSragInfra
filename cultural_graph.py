from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go

def generate_cultural_graph(df, app, anos):

    df['ANO'] = df['DATA_ALTA_OBITO'].dt.year    

    cultural_html = dbc.Col(children=[
                    html.H4(children='Distribuição dos Pacientes - Sexo/Idade', style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="ano-cultural-dropdown",
                        options=[{'label': str(ano), 'value': ano} for ano in anos],
                        value=anos[:2],
                        multi=True,
                    ),
                    html.Div([
                        dcc.Graph(
                            id='cultural-graph'
                        )
                    ])
    ])

    @app.callback(
        Output('cultural-graph', 'figure'),
        Input('ano-cultural-dropdown', 'value'),
    )
    def update_graph(anos_selecionados):
        # Dividir o conjunto de dados em homens e mulheres
        man = df[(df['SEXO'] == 'M') & (df['ANO'].isin(anos_selecionados))]
        woman = df[(df['SEXO'] == 'F') & (df['ANO'].isin(anos_selecionados))]

        # Criação do gráfico de barras
        bins = np.arange(0, 115, 5)

        # Calcular o número de homens e mulheres em cada intervalo de idade
        count_men, _ = np.histogram(man['IDADE'], bins=bins)
        count_women, _ = np.histogram(woman['IDADE'], bins=bins)

        fig = go.Figure(data=[
            go.Bar(
                name='Homens', 
                x=bins, 
                y=count_men,
                text=count_men,
                textposition='auto'
            ),
            go.Bar(
                name='Mulheres', 
                x=bins, 
                y=count_women,
                text=count_women,
                textposition='auto'
            )
        ])
        # Change the bar mode
        fig.update_layout(
            xaxis_tickfont_size=14,
            barmode='group',
            xaxis=dict(
                title='Idade',
                titlefont_size=16,
                tickfont_size=14,
            ),
            yaxis=dict(
                title='Qtd. Pessoas',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(orientation='h', yanchor='top', y=-0.2),
            autosize=True,
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )

        return fig


    return cultural_html