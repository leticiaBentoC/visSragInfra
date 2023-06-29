from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

def generate_media_graph(df, app, anos):
    # Converter a coluna 'DATA_NOTIFICACAO' para datetime, se necessário
    df['DATA_NOTIFICACAO'] = pd.to_datetime(df['DATA_NOTIFICACAO'])
    
    # Extrair o ano da data de notificação e adicionar como nova coluna
    df['ANO_NOTIFICACAO'] = df['DATA_NOTIFICACAO'].dt.year

    bar_chart = html.Div([
        html.H4(children='Gráfico de Barras de Dias de Internação', style={'textAlign': 'center'}),
        html.Div("Escolha o ano:"),
        dcc.Dropdown(
            id="anos-media-dropdown",
            value=anos[2],
            options=anos,
        ),
        dcc.Graph(id="media-chart")
    ])

    @app.callback(
        Output("media-chart", "figure"),
        Input("anos-media-dropdown", "value"),
    )
    def update_graph(ano, df=df):
        # Filtrar o DataFrame pelo ano selecionado
        df = df[df['ANO_NOTIFICACAO'] == ano]

        # Calcular a diferença de tempo de internação para cada paciente em dias
        tempos_internacao = [(alta - notificacao).days for notificacao, alta in zip(df['DATA_NOTIFICACAO'], df['DATA_ALTA_OBITO'])]

        # Criar uma Series com os tempos de internação e contar a quantidade de ocorrências para cada valor
        contagem_tempos_internacao = pd.Series(tempos_internacao).value_counts()

        # Ordenar a Series pelos valores dos tempos de internação
        contagem_tempos_internacao = contagem_tempos_internacao.sort_index()

        # Filtrar valores negativos da contagem de tempos de internação
        contagem_tempos_internacao = contagem_tempos_internacao[contagem_tempos_internacao.index >= 0]

        # Calcular a média de quantidade de dias de internação
        media_dias_internacao = (contagem_tempos_internacao.index * contagem_tempos_internacao).sum() / contagem_tempos_internacao.sum()

        # Criar o gráfico de barras
        fig = go.Figure()

        # Adicionar barras para a quantidade de dias de internação
        fig.add_trace(go.Bar(x=contagem_tempos_internacao.index, y=contagem_tempos_internacao, name='Quantidade de Dias de Internação'))

        # Adicionar uma linha para a média de dias de internação
        fig.add_trace(go.Scatter(x=[media_dias_internacao], y=[0], mode='markers', name='Média de Dias de Internação'))

        # Configurar o layout do gráfico
        fig.update_layout(
            xaxis=dict(title='Quantidade de Dias'),
            yaxis=dict(title='Contagem'),
            legend=dict(orientation='h', yanchor='top', y=-0.2),
            autosize=True,
        )

        return fig
    
    return bar_chart
