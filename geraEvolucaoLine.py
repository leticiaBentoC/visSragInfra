# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale

import data_tratamento_sintomas as dts

app = Dash(__name__)

# Faz a leitura dos datasets dos anos de 2020, 2021, 2022 e 2023
df = pd.read_csv('./dados/merged_dataset.csv', sep = ";", encoding='ISO-8859-1', on_bad_lines='skip', 
        low_memory=False, dayfirst=False, parse_dates=['DATA_ALTA_OBITO', 'DATA_NOTIFICACAO'])

output_file = './dados/line_dataset.csv'

df['DATA_ALTA_OBITO'] = pd.to_datetime(df['DATA_ALTA_OBITO'], format='%d/%m/%Y')

# Filtrar os registros onde "obito" é igual a 1 e agrupar por mês da coluna "data"
cura = df[df['EVOLUCAO_CASO'] == 1].groupby(pd.Grouper(key='DATA_ALTA_OBITO', freq='M')).size()
obito = df[df['EVOLUCAO_CASO'] == 2].groupby(pd.Grouper(key='DATA_ALTA_OBITO', freq='M')).size()
obito_outros = df[df['EVOLUCAO_CASO'] == 3].groupby(pd.Grouper(key='DATA_ALTA_OBITO', freq='M')).size()

# Reindexar as arrays para garantir o mesmo índice
cura = cura.reindex(obito.index)
obito_outros = obito_outros.reindex(obito.index)

df_casos = pd.DataFrame({'mes': obito.index, 'cura': cura.values, 'obito': obito.values, 'obito_outros': obito_outros.values})

# Salva o dataframe final no arquivo
df_casos.to_csv(output_file, sep=';', index=False, encoding='ISO-8859-1')

# LAYOUT
app.layout = html.Div("oi")

####################################################################################
# CALLBACK

####################################################################################
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
