from docxtpl import DocxTemplate
import pandas as pd


base = pd.DataFrame(columns=['Razao Social', "Cidade", "uf","Rua", "Número" ,"Cep"])
base.index.name = "cnpj"
base.to_csv("foo.csv")

print("base gerada")





