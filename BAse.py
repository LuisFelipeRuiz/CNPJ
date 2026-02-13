import requests
import numpy as np
import pandas as pd
from pathlib import Path
import time as t
import streamlit as st

df = pd.read_csv("foo.csv", index_col="cnpj", dtype={"cnpj": str})

def transforma_uf(uf):
    ufs = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
    }

    if not uf:
        return None

    return ufs.get(uf.upper(), uf)

def transforma_de(info):
    info = info.title()
    if " De " in info:
        return info.replace(" De "," de ")
    else:
        return info
    
def transforma_sao(info):
    info = info.title()
    if "Sao" in info:
        return info.replace("Sao","São")
    else:
        return info
    
def transforma_cep(cep):
    if(len(cep)!=8):
        cep = cep.zfill(8)
    return f"{cep[:5]}-{cep[5:]}"

        

def consultar_cnpj(cnpj):
    cnpj = cnpj.replace(".","").replace("-","").replace("/","").strip()
    if(len(cnpj)!=14):
        cnpj = cnpj.zfill(14)

    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

    tent = 0

    while tent<3:
        try:
            responde = requests.get(url, timeout=10)

            if responde.status_code != 200:
                tent+=1
                print(f"{tent}. Erro HTTP:{responde.status_code}, CNPJ: {cnpj}")
                t.sleep(1)
                continue

            dados = responde.json()
            break
    
        except requests.exceptions.RequestException as e:
            tent+=1
            print(f"Erro ao conectar na API: {e}, CNPJ: {cnpj}")
        
    else:
        print(f"Falha após 3 tentativas, CNPJ: {cnpj}")
        'CNPJ ', cnpj, 'invalido'
        return 0

    if cnpj in df.index:
        print(f'Já está na base: {cnpj}')
        'CNPJ ', cnpj, " Já está na base"
    else:
        print("CNPJ encontrado:", dados.get("cnpj"))
        df.loc[dados["cnpj"]] = [
            dados.get("razao_social"),
            transforma_de(transforma_sao(dados.get("municipio"))),
            transforma_uf(dados.get("uf")),
            transforma_de(dados.get("descricao_tipo_de_logradouro") + ' ' + dados.get("logradouro")),
            "n°" + dados.get("numero"),
            transforma_cep(dados.get("cep"))
        ]
        
                                

    df.to_csv("foo.csv")

        

def exportar_cnpj(df_base):

    df = pd.read_csv("foo.csv", index_col="cnpj", dtype={"cnpj": str})
    df_novo = pd.DataFrame(columns=['Razao Social', "Cidade", "uf","Rua", "Número" ,"Cep"])
    cnpj_lixo = []

    for cnpj in df_base['cnpj']:

        try:
            cnpj = (
                cnpj.replace(".", "")
                    .replace("-", "")
                    .replace("/", "")
                    .strip()
                    .zfill(14)
            )
        
            df_novo.loc[cnpj] = [
                df.loc[cnpj, 'Razao Social'],
                df.loc[cnpj, 'Cidade'],
                df.loc[cnpj, 'uf'],
                df.loc[cnpj, 'Rua'],
                df.loc[cnpj, 'Número'],
                df.loc[cnpj, 'Cep']
            ]
        except Exception as e:
            print(f"CNPJ ({cnpj}) com erro: {e}")
            cnpj_lixo.append(cnpj)

        
    if len(cnpj_lixo) != 0:
        print(cnpj_lixo)      

    df_novo.index.name = 'cnpj'
    df_novo.to_excel("CNPJs.xlsx")



if __name__ == "__main__":
    ### int main
    print("Escolha um opção:")
    print("1.Cnpj unitário\n2.Lista de Cnpjs")
    if(int(input("Opção: ")) == 1):
        cnpj = input("CNPJ:").replace(".","").replace("-","").replace("/","")
        consultar_cnpj(cnpj)
        if(int(input("Exportar CNPJ? 1 - Sim, 2 - Não: ")) == 1):
            df_base = pd.DataFrame({
                "cnpj": [cnpj]
            })
            exportar_cnpj(df_base)
    else:
        caminho = input("Informe o Caminho do Excel: ").strip()
        arquivo = Path(caminho)
        #precisa baixar Openpyxl
        #C:\Users\Luisão\OneDrive\Área de Trabalho\Teste.xlsx
        df_base = pd.read_excel(arquivo, 
                                engine="openpyxl",
                                dtype={"cnpj": str})
        
        for i in range(0, len(df_base.index)):
            consultar_cnpj(df_base.loc[i, "cnpj"])
        if(int(input("Exportar CNPJ? 1 - Sim, 2 - Não: ")) == 1):
            exportar_cnpj(df_base)

    
    

    print("tudo certo")
    if(int(input('Quer a tabela?:')) == 1):
        print(df)

