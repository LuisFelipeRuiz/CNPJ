import numpy as np
import pandas as pd
from docxtpl import DocxTemplate
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile

df = pd.read_csv("foo.csv", index_col="cnpj", dtype={"cnpj": str})

def transforma_de(info):
    info = info.title()
    if " De " in info:
        return info.replace(" De "," de ")
    else:
        return info

def formatar_cnpj(cnpj):
    cnpj = str(cnpj).zfill(14)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def criar_master(df_base, tempo):

    zip_buffer = BytesIO()
    total = len(df_base)
    i=0

    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    ano, mes, dia = tempo.split("-")
    tempo_ext = f"{dia} de {meses[int(mes)-1]} de {ano}"
    tempo = f"{dia}/{mes}/{ano}"
    

    try:
        with open("Master - .docx", "rb") as f:
            template_bytes = f.read()
    except Exception as e:
        raise Exception(f"Erro ao abrir template: {e}")
    
    with ZipFile(zip_buffer, "w") as zip_file:

        for i, cnpj in enumerate(df_base['cnpj']):

            cnpj = (
                    cnpj.replace(".", "")
                        .replace("-", "")
                        .replace("/", "")
                        .strip()
                        .zfill(14)
                )
            
            if cnpj not in df.index:
                continue

            context = {
                "CNPJ" : formatar_cnpj(cnpj),
                "Fornecedor" : df.loc[cnpj, "Razao Social"],
                "Cidade" : df.loc[cnpj, "Cidade"],
                "Estado" : df.loc[cnpj, "uf"],
                "Rua" : df.loc[cnpj, "Rua"],
                "Numero": df.loc[cnpj, "Número"],
                "Cep": df.loc[cnpj, "Cep"],
                'data' : tempo, 
                'Data' : tempo_ext  
            }
            
            doc = DocxTemplate(BytesIO(template_bytes))

            doc.render(context)

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            Nome = (df.loc[cnpj, "Razao Social"]).split()
            Nome = " ".join(Nome[:4])
            Nome = transforma_de(Nome) 

            zip_file.writestr(f"Master - {Nome}.docx", 
                              buffer.read())
            
            yield (i+1)/total, None 

    zip_buffer.seek(0)
    yield 1, zip_buffer

        

    


if __name__ == "__main__":
    print("Escolha um opção:")
    print("1.Cnpj unitário\n2.Lista de Cnpjs")
    if(int(input("Opção: ")) == 1):
        cnpj = input("CNPJ:").replace(".","").replace("-","").replace("/","")
        df_base = pd.DataFrame({
            "cnpj": [cnpj]
        })
        x = int(input("Escolha o Documento:\n1.Master: "))
        if(x==1):
            data = input("Inserir data(DD/MM/20AA): ")
            criar_master(df_base, data)


    else:
        caminho = input("Informe o Caminho do Excel: ").strip()
        arquivo = Path(caminho)
        #precisa baixar Openpyxl
        #C:\Users\Luisão\OneDrive\Área de Trabalho\Teste.xlsx
        df_base = pd.read_excel(arquivo, 
                                engine="openpyxl",
                                dtype={"cnpj": str})
        
        x = int(input("Escolha o Documento:\n1.Master: "))
        if(x==1):
            data = input("Inserir data(DD/MM/20AA): ")
            criar_master(df_base, data)

    
    

