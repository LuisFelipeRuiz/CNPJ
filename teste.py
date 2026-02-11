"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

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

Func = st.selectbox(
    "Qual funcionalidade?",
    ["Importar/Exportar CNPJ", "Gerar Documento"]
)

if Func == "Gerar Documento":
    gerencias = ["I", "II", "III", "IV"]

    # Categorias dependentes
    categorias = {
        "I": ["Jud", "Cob"],
        "II": ["Adm", "Fin"],
        "III": ["Cont", "Fiscal"],
        "IV": ["RH", "TI"]
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


else:
    Cnpj = st.selectbox(
    "Quantos CNPJS?",
    ["1", "2+ CNJS"])

    if Cnpj == 1:
        x = st.text_input("CNPJ:")
        buscacnpj(x)
        Deseja exportar ou ver a planilha completa?
        

