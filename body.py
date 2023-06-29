from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

import data_tratamento_sintomas as dts
import evolution
import line
import geo
import bar
import heatmap
import outlier_significance
import cultural_graph
import media

def generate_body(app):

    # Faz a leitura dos datasets dos anos de 2020, 2021, 2022 e 2023
    df = pd.read_csv('./dados/merged_dataset.csv', sep = ";", encoding='ISO-8859-1', on_bad_lines='skip', 
            low_memory=False, dayfirst=False, parse_dates=['DATA_ALTA_OBITO', 'DATA_NOTIFICACAO'])

    # Lista de anos
    anos = [2019, 2020, 2021, 2022, 2023]

    df_casos = pd.read_csv('./dados/line_dataset.csv', sep = ";", encoding='ISO-8859-1', on_bad_lines='skip', 
        low_memory=False)

    # df_sintomas = dts.generate_tratamento_sintomas(df)
    df_sintomas = pd.read_csv('./dados/sintomas_dataset.csv', sep = ";", encoding='ISO-8859-1', on_bad_lines='skip', 
        low_memory=False)
    
    evolutionCards = evolution.generate_cards(df)
    htmlLine = line.generate_line_chart(df_casos, app, anos)
    # htmlGeo = geo.generate_geo_graph(df, app)
    # htmlBar = bar.generate_bar_graph(df, app, anos)
    # htmlHeatmap = heatmap.generate_heatmap_grapf()
    # htmlOutlier = outlier_significance.generate_outlier_grapf(df_sintomas, app)
    # htmlCultural = cultural_graph.generate_cultural_graph(df, app, anos)
    # htmlMedia = media.generate_media_graph(df, app, anos)
    
    body = html.Div(
    [
        dbc.Container([evolutionCards], class_name="mb-5 container-fluid"),
        dbc.Container([
            htmlLine, 
            html.Hr()
        ], class_name="mb-5 container-fluid"),
        # dbc.Container([
        #     htmlGeo, 
        #     html.Hr()
        # ], class_name="mb-5 container-fluid"),
        # dbc.Container([
        #     htmlBar, 
        #     html.Hr()
        # ], class_name="mb-5 container-fluid"),
        # dbc.Container([
        #     htmlOutlier,
        #     html.Hr(),
        #     htmlHeatmap, 
        #     html.Hr()
        # ], class_name="mb-5 container-fluid"),
        # dbc.Container([
        #     htmlCultural,
        #     html.Hr()
        # ], class_name="mb-5 container-fluid"),
        # dbc.Container([
        #     htmlMedia, 
        #     html.Hr()
        # ], class_name="mb-5 container-fluid"),
        html.Hr(),
    ],
)
    return body