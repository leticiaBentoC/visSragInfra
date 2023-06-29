import pandas as pd

import col_indesejadas as ci
import col_sintomas as cs

def generate_tratamento_sintomas(df):
    nomes_colunas = cs.generate_col_sintomas()

    # Itens que serão excluídos do array
    itens_indesejados = ci.generate_col_indesejadas() 
    
    # Cria uma cópia de nomes_colunas
    sintomas = [col for col in nomes_colunas if col not in itens_indesejados]

    # seta um novo dataset somente com as colunas existentes no dataset importado
    df_sintomas = pd.DataFrame()
    for col in sintomas:
        if col in df.columns:
            df_sintomas[col] = df[col]
    
    return df_sintomas
