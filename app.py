# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale

import header as h
import body
import gc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, 'styles.css'], title='Visualização de Dados SRAG')

gc.collect()

# # Faz a leitura dos datasets dos anos de 2020, 2021, 2022 e 2023
# df_final = pd.read_csv('./dados/merged_dataset.csv', sep = ";", encoding='ISO-8859-1', on_bad_lines='skip', 
#         low_memory=False, dayfirst=False, parse_dates=['DATA_ALTA_OBITO', 'DATA_NOTIFICACAO'])

# gera o CABEÇALHO
navbar = h.generate_header()

# # Gera o corpo
htmlBody = body.generate_body(app)

# LAYOUT
app.layout = html.Div([
    navbar,
    htmlBody,
])

####################################################################################
# CALLBACK

####################################################################################
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
