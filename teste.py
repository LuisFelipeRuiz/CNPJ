"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import BAse
import basele
import time as t

# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })

# df

# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])

# 'You selected: ', option

# streamlit run teste.py
def dataload():
    df_base = st.file_uploader("Choose a file", type = 'xlsx')
    return df_base

Func = st.selectbox(
    "Qual funcionalidade?",
    ["Importar/Exportar CNPJ", "Gerar Documento"]
)

if Func == "Gerar Documento":
    gerencias = ["I", "II"]

    # Categorias dependentes
    categorias = {
        "I": ["Jurídico", "Cobrança","Viagens"],
        "II": ["Call Center", "BPO"],
    }

    # Select da Gerência
    gerencia_sel = st.selectbox(
        "Qual Gerência?",
        gerencias
    )

    # Select dependente da Categoria
    categoria_sel = st.selectbox(
        "Qual Categoria?",
        categorias[gerencia_sel]
    )
    'You selected: ', categoria_sel, 'oi'


else:
    Cnpj = st.selectbox(
    "Quantos CNPJS?",
    ["1", "2+ CNJS"])

    if Cnpj == "1":
        x = st.text_input("CNPJ:")
        x = (
                    x.replace(".", "")
                        .replace("-", "")
                        .replace("/", "")
                        .strip()
                        .zfill(14)
                )
        
        y = BAse.consultar_cnpj(x)
        if(y==0):
            'CNPJ invalido'
        else:
            'CNPJ na base'
            df = pd.read_csv("foo.csv", index_col="cnpj", dtype={"cnpj": str})
            df.loc[x]
    else:
        
        df_base = dataload()
        if df_base != None:
            df_base = pd.read_excel(df_base, 
                                engine="openpyxl",
                                dtype={"cnpj": str})
            df_base
            for i in range(0, len(df_base.index)):
                y = BAse.consultar_cnpj(df_base.loc[i, "cnpj"])
                if(y==0):
                    'CNPJ', df_base.loc[i, "cnpj"],'invalido'
                    t.sleep(1)
                else:
                    'CNPJ na base'
                


            

        



        

