# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale

import data
import json

app = Dash(__name__)

config = json.load(open("config.json"))
# Cria uma lista com os nomes dos arquivos dos datasets
dataset_files = [config['dataset_2019'], config['dataset_2020'], config['dataset_2021'], config['dataset_2022'], config['dataset_2023']]

# Definir as colunas do novo dataset
colunas = ['DATA_NOTIFICACAO', 'SEMANA_NOTIFICACAO', 'DATA_PRIMEIROS_SINTOMAS',
        'SEMANA_PRIMEIROS_SINTOMAS', 'UF', 'ID_REGIONAL', 'CODIGO_REGIONAL',
        'ID_MUNICIPIO', 'CODIGO_MUNICIPIO', 'ID_UNIDADE_SAUDE', 
        'CODIGO_UNIDADE_SAUDE', 'SEXO', 'DATA_NASCIMENTO', 'IDADE',
        'TIPO_IDADE', 'IDADE_GESTACIONAL', 'RACA', 'ESCOLARIDADE',
        'CODIGO_PAIS', 'SIGLA_UF', 'ID_RESIDENCIA_PACIENTE', 
        'CODIGO_RESIDENCIA_PACIENTE', 'ID_MUNICIPIO_RESIDENCIA', 'CODIGO_MUNICIPIO_RESIDENCIA',
        'ZONA', 'DESCONFORTO_RESPIRATORIO', 'OUTROS_SINTOMAS', 'HOUVE_INTERNACAO',
        'DATA_INTERNACAO', 'UF_INTERNACAO', 'ID_REGIONAL_INTERNACAO', 
        'CODIGO_REGIONAL_INTERNACAO', 'ID_MUNICIPIO_INTERNACAO', 'CODIGO_MUNICIPIO_INTERNACAO',
        'SUPORTE_VENTILATORIO', 'RESULTADO_RAIOX', 'COLETOU_AMOSTRA', 'DATA_COLETA',
        'TIPO_AMOSTRA', 'RESULTADO_PCR', 'DATA_RESULTADO_PCR', 'CASO_FINAL',
        'CRITERIO_ENCERRAMENTO', 'EVOLUCAO_CASO', 'DATA_ALTA_OBITO', 'DATA_ENCERRAMENTO',
        'DATA_DIGITACAO', 'DOR_ABDOMINAL', 'PERDA_OLFATO', 'PERDA_PALADAR',
        'RESULTADO_TOMOGRAFIA', 'RESULTADO_ANTIGENICO', 'ESTRANGEIRO', 'VACINA_COVID',
        'INFO_VACINA_COVID']

output_file = './dados/merged_dataset.csv'
colunas = [...]  # Colunas definidas do dataframe

# Cria o dataframe vazio com as colunas definidas
df_merged = pd.DataFrame(columns=colunas)

# Loop para ler e adicionar os datasets ao novo dataframe
for file in dataset_files:
    df = pd.read_csv(file, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', nrows=790000, low_memory=False, dayfirst=True,
                     parse_dates=['DT_NOTIFIC', 'DT_SIN_PRI', 'DT_NASC', 'DT_INTERNA', 'DT_COLETA', 'DT_PCR', 'DT_EVOLUCA',
                                  'DT_ENCERRA', 'DT_DIGITA'])
    df_final = data.trata_dados(df)
    
    # Adiciona os dados do dataframe atual ao novo dataframe
    df_merged = pd.concat([df_merged, df_final], ignore_index=True)
    
    # Grava o dataframe no arquivo em cada iteração
    # df_merged.to_csv(output_file, sep=';', index=False, encoding='ISO-8859-1')

# Salva o dataframe final no arquivo
df_merged.to_csv(output_file, sep=';', index=False, encoding='ISO-8859-1')

# LAYOUT
app.layout = html.Div("oi")

####################################################################################
# CALLBACK

####################################################################################
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
