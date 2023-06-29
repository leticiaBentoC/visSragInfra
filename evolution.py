from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime

def generate_cards(df):
    # Função para criar o componente Card
    def create_card(title, value1, value2, value3):
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Span([dbc.Badge(title, color="secondary", className="me-1 float-sm-end")]),
                        html.Div(
                            [
                                html.Span("Casos Curados"),
                                html.H3(value1, style={"color": "#adfc92"}, className="card-text mb-0"),
                            ],
                            className="card-item",
                        ),
                        html.Div(
                            [
                                html.Span("Óbitos por SRAG"),
                                html.H3(value2, style={"color": "indianred"}, className="card-text mb-0"),
                            ],
                            className="card-item",
                        ),
                        html.Div(
                            [
                                html.Span("Óbitos"),
                                html.H3(value3, style={"color": "purple"}, className="card-text mb-0"),
                            ],
                            className="card-item",
                        ),
                    ]
                )
            ],
            color="light",
            outline=True,
            className="mt-2 shadow",
        )
    
    # Converta a coluna DATA_ALTA_OBITO para o tipo datetime
    df['DATA_ALTA_OBITO'] = pd.to_datetime(df['DATA_ALTA_OBITO'], format='%d/%m/%Y')

    # Obter os anos presentes na coluna 'DATA_ALTA_OBITO' e ordená-los em ordem crescente
    anos = np.sort(df['DATA_ALTA_OBITO'].dt.year.unique())

    # Criar uma lista para armazenar as colunas dos cards
    colunas = []

    # Loop para percorrer os anos e criar os cards correspondentes
    for ano in anos:
        # Filtrar os casos pelo ano
        casos_ano = df[df['DATA_ALTA_OBITO'].dt.year == ano]

        # Filtrar e Contar o número total de casos para o ano
        total_cura = casos_ano[casos_ano['EVOLUCAO_CASO'] == 1].shape[0]
        total_obito_srag = casos_ano[casos_ano['EVOLUCAO_CASO'] == 2].shape[0]
        total_obito = casos_ano[casos_ano['EVOLUCAO_CASO'] == 3].shape[0]

        # Substituir a vírgula pelo ponto
        cura_formatada = "{:,}".format(total_cura).replace(",", ".")  
        obito_srag_formatado = "{:,}".format(total_obito_srag).replace(",", ".")
        obito_formatado = "{:,}".format(total_obito).replace(",", ".")

        # Criar o card com o título do ano e o valor total de casos
        card = create_card(ano, cura_formatada, obito_srag_formatado, obito_formatado)

        # Criar a coluna com o card do ano
        coluna = dbc.Col(card, className="mt-2")

        # Adicionar a coluna à lista de colunas
        colunas.append(coluna)

    # Criar o layout com as colunas
    layout = dbc.Container(
        [
            dbc.Row(colunas, className="mt-4"),
        ],
        fluid=True,
    )

    return layout
