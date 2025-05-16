import streamlit as st
import pandas as pd
import os

st.title("Medição de Obra")

# Caminho para o arquivo na mesma pasta do script
excel_file = "medicao.xlsx"

if not os.path.exists(excel_file):
    st.error(f"Arquivo {excel_file} não encontrado na pasta do projeto! Por favor, coloque o arquivo na mesma pasta que este script.")
    st.stop()

# Carregar dados da planilha
df = pd.read_excel(excel_file)

# Verificar se as colunas essenciais existem
colunas_necessarias = {"Local", "Serviço", "Unidade"}
if not colunas_necessarias.issubset(df.columns):
    st.error(f"Colunas necessárias não encontradas na planilha. Precisa ter: {colunas_necessarias}")
    st.stop()

# Criar um dataframe para armazenar as medições
df["Medição"] = 0.0

# Interface para entrada de medição por linha
for idx, row in df.iterrows():
    st.write(f"**Local:** {row['Local']} - **Serviço:** {row['Serviço']} - **Unidade:** {row['Unidade']}")
    medicao = st.number_input(f"Medição para {row['Local']} - {row['Serviço']}", min_value=0.0, value=0.0, key=idx)
    df.at[idx, "Medição"] = medicao

if st.button("Exportar Medições para Excel"):
    output_file = "medicao_exportada.xlsx"
    df.to_excel(output_file, index=False)
    st.success(f"Medições exportadas com sucesso para {output_file}")
    st.markdown(f"[Baixar arquivo exportado](./{output_file})")
