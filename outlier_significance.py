from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import phik

def generate_outlier_grapf(df_sintomas, app):

    sintomas = ['DISPNEIA', 'SATURACAO', 'DESCONFORTO_RESPIRATORIO', 'TOSSE', 'FEBRE']

    radio_buttons = html.Div([
        dbc.RadioItems(
            id='sintomas-radio',
            class_name="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[{'label': sintoma, 'value': sintoma} for sintoma in sintomas],
            inline=True,
            value=sintomas[0],
    )],
        className="radio-group",
    )
    
    outlier_html = dbc.Col(children=[
        html.Div([
            html.H4(children='Outlier Significance', style={'textAlign': 'center'}),
            radio_buttons,
            dcc.Graph(id='outlier-graph')
        ])
    ])

    @app.callback(
        Output('outlier-graph', 'figure'),
        Input('sintomas-radio', 'value')
    )
    def update_outlier_graph(sintoma):
        x, y = df_sintomas[['EVOLUCAO_CASO', sintoma]].T.values

        phik.outlier_significance_from_array(x, y, num_vars=['x'])

        outlier_signifs = phik.outlier_significance_from_array(x, y, num_vars=['x'])

        fig = px.imshow(outlier_signifs, 
                        labels=dict(x=sintoma, y="Evolução do Caso", color="Productivity"),
                        x=['Sim', 'Não', 'Ignorados'],
                        y=['Cura', 'Óbito SRAG', 'Óbito por outras causas', 'Ignorados'],
                        text_auto=True)

        return fig

    return outlier_html