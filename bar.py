from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

import col_sintomas as cs
import col_indesejadas as ci

def generate_bar_graph(df, app, anos):
    nomes_colunas = cs.generate_col_sintomas()

    # Itens que serão excluídos do array
    itens_indesejados = ci.generate_col_indesejadas() 
    
    # Cria uma cópia de nomes_colunas
    sintomas = [col for col in nomes_colunas if col not in itens_indesejados] 

    df['ANO'] = df['DATA_ALTA_OBITO'].dt.year

    button_group = html.Div([
        dbc.RadioItems(
            id="evolucao-radio",
            class_name="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {'label': 'Cura', 'value': 1},
                {'label': 'Óbito SRAG', 'value': 2},
                {'label': 'Óbito por outras causas', 'value': 3}
            ],
            value=2,
        )],
        className="radio-group",
    )

    htmlControl = dbc.Col(
        [
            html.Div([
                html.H4(children='Sintomas mais frequentes', style={'textAlign': 'center'}),
                button_group,
                dcc.Dropdown(
                    id="ano-dropdown",
                    options=[{'label': str(ano), 'value': ano} for ano in anos],
                    value=anos[:3],
                    multi=True,
                ),
                dcc.Graph(id="bar-graph"),
            ])
        ]
    )

    @app.callback(
        Output('bar-graph', 'figure'),
        Input('ano-dropdown', 'value'),
        Input('evolucao-radio', 'value')
    )
    def update_graph(anos_selecionados, evolucao_selecionada):
        # Cria um dicionário vazio para armazenar os resultados
        valor = {}

        # Iterar sobre cada sintoma
        for col in sintomas:
            if col in df.columns:
                valor[col] = {}
                
                # Iterar sobre cada ano
                for ano in anos:
                    df_ano_sintoma = df.loc[(df[col] == 1) & (df['ANO'] == ano) & (df['EVOLUCAO_CASO'] == evolucao_selecionada)]
                    count_sim = df_ano_sintoma.shape[0]
                    valor[col][ano] = count_sim

                
        # Criar um DataFrame a partir do dicionário de valores
        df_bar = pd.DataFrame(valor)

        # Transpor o DataFrame para ter os sintomas como colunas
        df_bar = df_bar.T.reset_index()

        # Renomear as colunas
        df_bar.columns = ['sintoma'] + anos

        # Calcular a soma das colunas de anos e adicionar uma nova coluna "total"
        df_bar['total'] = df_bar[anos].sum(axis=1)

        # Ordenar o DataFrame com base na coluna "total" de forma decrescente
        df_bar = df_bar.sort_values(by='total', ascending=True)

        # Definir as cores para cada ano
        cores = ['steelblue', 'limegreen', 'gold', 'indianred', 'purple']

        # Remover EVOLUCAO_CASO dos sintomas, para não criar uma barra para a evolução
        df_filtered = df_bar.drop(df_bar[df_bar['sintoma'] == 'EVOLUCAO_CASO'].index)

        df_filtered = df_filtered.loc[df_filtered['sintoma'] != 'total', ['sintoma'] + anos_selecionados]

        # Ordenar o DataFrame com base na coluna do ano selecionado de forma decrescente
        df_filtered = df_filtered.sort_values(by=anos_selecionados[0], ascending=True)

        # Criar uma lista de barras empilhadas para o ano selecionado
        barras = []
        for i, ano in enumerate(anos_selecionados):
            barras.append(go.Bar(
                y=df_filtered['sintoma'],
                x=df_filtered[ano],
                name=str(ano),
                orientation='h',
                marker=dict(color=cores[i])
            ))

        # Criar o layout do gráfico
        layout = go.Layout(
            barmode='stack',
            xaxis=dict(title='Total'),
            yaxis=dict(title='Sintoma'),
            height=600  # Ajuste a altura do quadro conforme necessário
        )

        # Criar a figura do gráfico
        fig = go.Figure(data=barras, layout=layout)

        return fig

    return htmlControl
