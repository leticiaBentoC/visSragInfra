from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from phik.binning import bin_data

def generate_heatmap_grapf():    
    # Carregar a matriz a partir do arquivo
    phik_overview = pd.read_csv('./dados/phik_matrix.csv', index_col=0)

    # PLOTLY
    fig = go.Figure(data=go.Heatmap(
        z=phik_overview,
        x=phik_overview.columns,
        y=phik_overview.index,
        colorscale='Blues',
        zmin=0,
        zmax=1
    ))

    fig.update_layout(
        title="Correlação φK",
        xaxis=dict(title="Sintomas"),
        yaxis=dict(title="Sintomas"),
        autosize=False,
        width=900,
        height=850,
        font=dict(size=14)
    )

    heatmap_html = dbc.Col(children=[
        html.H4(children='Heatmap - Sintomas', style={'textAlign': 'center'}),
        html.Div([
            dcc.Graph(
                id='heatmap-graph',
                figure=fig,
            )
        ])
    ])
    return heatmap_html
    