from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

def generate_line_chart(df_casos, app, anos): 
    line = html.Div([
        html.H4(children='Evolução dos Casos', style={'textAlign': 'center'}),
        html.Div("Escolha o ano:"),
        dcc.Dropdown(
            id="years-dropdown",
            value=anos[:2],
            options=anos,
            multi=True,
        ),
        dcc.Graph(id="line-chart")
    ])

    @app.callback(
        Output("line-chart", "figure"),
        Input("years-dropdown", "value"),
    )
    def update_graph(years, df_casos=df_casos):

        df_casos['mes'] = pd.to_datetime(df_casos['mes'])
        df_casos['ano'] = df_casos['mes'].dt.year

        # Filtrar os dados usando comparações numéricas diretas
        filtered_df = df_casos[df_casos['ano'].isin(years)]
        # df_casos['mes'] = pd.to_datetime(df_casos['mes'])
        # filtered_df = df_casos[df_casos['mes'].dt.year.isin(years)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['mes'], y=filtered_df['cura'], mode='lines+markers', name='Cura'))
        fig.add_trace(go.Scatter(x=filtered_df['mes'], y=filtered_df['obito'], mode='lines+markers', name='Óbito por SRAG'))
        fig.add_trace(go.Scatter(x=filtered_df['mes'], y=filtered_df['obito_outros'], mode='lines+markers', name='Óbito por outras causas'))

        fig.update_layout(
            xaxis=dict(title='Mês'),
            yaxis=dict(title='Quantidade de Casos'),
            legend=dict(orientation='h', yanchor='top', y=-0.2),
            autosize=True,
        )

        return fig
    
    return line

