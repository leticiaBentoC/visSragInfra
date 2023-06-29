# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale
import numpy as np
import phik
from phik import phik_matrix

app = Dash(__name__)

# Faz a leitura do dataset de sintomas
df_sintomas = pd.read_csv('./dados/sintomas_dataset.csv', sep = ";", encoding='ISO-8859-1', on_bad_lines='skip', 
        low_memory=False)

# Remova a coluna "EVOLUCAO_CASO"
df_sintomas = df_sintomas.drop('EVOLUCAO_CASO', axis=1)

data_types = {'NOSOCOMIAL': 'interval',
             'AVE_SUINO':'interval',
             'FEBRE':'ordinal',
             'TOSSE':'interval',
             'GARGANTA':'categorical',
             'DISPNEIA':'categorical',
             'DESCONFORTO_RESPIRATORIO':'categorical',
             'SATURACAO':'categorical'}
interval_cols = [col for col, v in data_types.items() if v=='categorical' and col in df_sintomas.columns]

# Calcular a matriz de correlação phi_k
phik_overview = df_sintomas.phik_matrix(interval_cols=interval_cols)

# Converter a matriz em um DataFrame
phik_df = pd.DataFrame(phik_overview)

# Gravar o DataFrame em um arquivo CSV
phik_df.to_csv('./dados/phik_matrix.csv', index=True)

# LAYOUT
app.layout = html.Div("oi")

####################################################################################
# CALLBACK

####################################################################################
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
