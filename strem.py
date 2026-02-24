import streamlit as st
import pandas as pd
import BAse
import basele
import time as t
from io import BytesIO
from docx import Document
import zipfile

def dataload():
    df_base = st.file_uploader("Choose a file", type = 'xlsx')
    return df_base

def Documentos(doc):
        def fazer_lista():
            t.sleep(1)
            return "cnpj".encode("utf-8")
        
        col1,col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Lista",
                data=fazer_lista,
                file_name="Lista.csv",
                mime="text/csv",
                width="stretch",
                type = 'primary'
            )
        with col2:
            data = None
            if doc == "MC":
                with open("Master - .docx", "rb") as file:
                    docx_bytes = file.read()
                st.download_button(
                    label="Baixar modelo",
                    data=docx_bytes,
                    file_name="Master Cível.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

        if doc =='MC':
            data = st.date_input("Data(00/00/0000):", 
                              width='stretch',
                              value = None,
                              format="DD/MM/YYYY")
            if data is None:
                pass
                
        df_base = dataload()
        if df_base is None:
            pass
        if df_base != None:
            df_base = pd.read_excel(df_base, 
                                engine="openpyxl",
                                dtype={"cnpj": str})
            base = st.empty()
            base.write(df_base.head())

            status = st.empty()
            cnpj_lixo = []

            for i in range(0, len(df_base.index)):
                y = BAse.consultar_cnpj(df_base.loc[i, "cnpj"])

                if(y==0):
                    cnpj_lixo.append(df_base.loc[i, "cnpj"])

            t.sleep(0.5)
            if len(cnpj_lixo) != 0:
                'CNPJs Invalidos:', cnpj_lixo


            return data, df_base
        
        return None, None

if "gerando" not in st.session_state:
    st.session_state.gerando = False

if "pronto" not in st.session_state:
    st.session_state.pronto = False

if "zip" not in st.session_state:
    st.session_state.zip = None

if "progresso" not in st.session_state:
    st.session_state.progresso = 0
        

if 'logged' not in st.session_state:
    st.session_state.logged = False

@st.dialog("Alert")
def login_validation(usr, passw):
    if usr == '' or passw == '':
        st.error("Please enter your username or password.")
    else:
        st.success("Login sucessful")
        t.sleep(1)
        st.session_state.logged = True
        st.rerun()


if not st.session_state.logged:

    with st.form('sign_in'):
        st.title('Sign in')
        st.caption("Enter your username and password")
        st.divider()
        username = st.text_input("Username")
        password = st.text_input("Password",
                                type= 'password')

        submit = st.form_submit_button(label='Submit',
                                    type='primary',
                                    use_container_width='true')

    if submit:
        login_validation(username, password)

else:

    Func = st.selectbox(
        "Qual funcionalidade?",
        ["Importar/Exportar CNPJ", "Gerar Documento"]
    )

    if Func == "Gerar Documento":
        gerencias = ["I", "II", "III"]

        # Categorias dependentes
        categorias = {
            "I": ["Jurídico", "Cobrança","Viagens"],
            "II": ["Call Center", "BPO"],
            "III": ["Jurídico"]
        }

        documentos = {
            "Jurídico": ["Master Cível","Master Trabalhista","TSS Cível", "TSS Trabalhista"]
        }

        # Select da Gerência
        gerencia_sel = st.selectbox(
            "Qual Gerência?",
            gerencias
        )

        # Select dependente da Categoria
        col1,col2 = st.columns(2)
        with col1: 
            categoria_sel = st.selectbox(
                "Qual Categoria?",
                categorias[gerencia_sel]
            )
        
        with col2:
            documentos_sel = st.selectbox(
                "Qual documento?",
                documentos[categoria_sel])
            
        st.write(" ")
            
        if documentos_sel == "Master Cível":
            doc = "MC"
            data, df_base = Documentos(doc) 
            status = st.empty()

            if df_base is not None and data is not None:

                progresso_bar = st.progress(0)
                texto = st.empty()

                if not st.session_state.gerando and not st.session_state.pronto:
                    gerar = st.button("Gerar documentos",
                                      width="stretch")
                    if gerar:

                        st.session_state.gerando = True

                        for progresso, zip_file in basele.criar_master(df_base, str(data)):

                            progresso_bar.progress(progresso)
                            texto.text(f"{int(progresso*100)}% concluído")

                            if zip_file is not None:
                                st.session_state.zip = zip_file
                                st.session_state.pronto = True
                                st.session_state.gerando = False
                                st.rerun()

                if st.session_state.pronto:

                    st.download_button(
                        label="Baixar Docs",
                        data=st.session_state.zip,
                        file_name="Documentos.zip",
                        mime="application/zip",
                        width='stretch',
                        type='primary'
                    )
                    
            

    else:
        Cnpj = st.selectbox(
        "Quantos CNPJS?",
        ["1", "2+ CNJS"])

        if Cnpj == "1":
            x = st.text_input("CNPJ:",
                              value= None)
            status = st.empty()
            if(x==None):
                pass
            else:
                status.text("Verificando CNPJ...")
                x = (
                            x.replace(".", "")
                                .replace("-", "")
                                .replace("/", "")
                                .strip()
                                .zfill(14)
                        )
                y = BAse.consultar_cnpj(x)
                if(y==0):
                    status.text('CNPJ invalido')
                else:
                    status.text('CNPJ na base')
                    df = pd.read_csv("foo.csv", index_col="cnpj", dtype={"cnpj": str})
                    df.loc[x]
        else:

            def fazer_lista():
                t.sleep(1)
                return "cnpj".encode("utf-8")

            st.download_button(
                label="Download Lista",
                data=fazer_lista,
                file_name="Lista.csv",
                mime="text/csv",
                width="stretch",
                type = 'primary'
            )

            df_base = dataload()
            if df_base != None:
                df_base = pd.read_excel(df_base, 
                                    engine="openpyxl",
                                    dtype={"cnpj": str})
                base = st.empty()
                base.write(df_base.head())

                status = st.empty()
                cnpj_lixo = []

                for i in range(0, len(df_base.index)):
                    y = BAse.consultar_cnpj(df_base.loc[i, "cnpj"])

                    if(y==0):
                        status.text(f'CNPJ {df_base.loc[i, "cnpj"]} invalido')
                        cnpj_lixo.append(df_base.loc[i, "cnpj"])
                    
                    else:
                        status.text(f'CNPJ {df_base.loc[i, "cnpj"]} na base')

                t.sleep(0.5)
                status.text("Import finalizado")
                base.empty()
                if len(cnpj_lixo) != 0:
                    'CNPJs Invalidos:', cnpj_lixo
                
                df_novo = BAse.exportar_cnpj(df_base)
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_novo.to_excel(writer, index=False, sheet_name='Base')

                excel_data = output.getvalue()

                st.download_button(
                    label="Exportar Base inserida",
                    data=excel_data,
                    file_name="Base.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type='secondary'
                )
                    
                
