import streamlit as st
import pandas as pd
import os

st.title("Medição de Obra - App")

# --- Caminho da planilha ---
DATA_DIR = "data"
ARQUIVO_PLANILHA = os.path.join(DATA_DIR, "medicao.xlsx")

# Cria a pasta se não existir
os.makedirs(DATA_DIR, exist_ok=True)

# --- Leitura da planilha ---
@st.cache_data
def carregar_planilha(caminho):
    df = pd.read_excel(caminho)
    # Ajusta colunas para minúsculas e sem espaços
    df.columns = df.columns.str.strip().str.lower()
    return df

if not os.path.exists(ARQUIVO_PLANILHA):
    st.error(f"Arquivo {ARQUIVO_PLANILHA} não encontrado! Coloque a planilha no diretório 'data'.")
    st.stop()

df = carregar_planilha(ARQUIVO_PLANILHA)

# Mostrar colunas para depurar
st.write("Colunas encontradas na planilha:", df.columns.tolist())

# --- Verifica se colunas necessárias existem ---
colunas_necessarias = ['local', 'serviço', 'unidade']

if not all(col in df.columns for col in colunas_necessarias):
    st.error(f"A planilha deve conter as colunas: {colunas_necessarias}")
    st.stop()

# --- Seleção Local e Serviço ---
local_selecionado = st.selectbox("Selecione o Local:", options=df['local'].unique())
df_filtrado = df[df['local'] == local_selecionado]

servico_selecionado = st.selectbox("Selecione o Serviço:", options=df_filtrado['serviço'].unique())
df_servico = df_filtrado[df_filtrado['serviço'] == servico_selecionado]

st.write(f"Unidade do serviço: {df_servico['unidade'].values[0]}")

# --- Entrada da medição ---
medicao = st.number_input("Digite a medição (%) para este serviço:", min_value=0.0, max_value=100.0, step=0.1)

# --- Botão para salvar ---
if st.button("Salvar medição"):

    # Adiciona ou atualiza uma coluna 'medição' no DataFrame original para essa linha
    idx = df_servico.index[0]  # Pega o índice correto
    df.at[idx, 'medição'] = medicao

    # Salva tudo no Excel (substitui o arquivo)
    df.to_excel(ARQUIVO_PLANILHA, index=False)

    st.success(f"Medição de {medicao}% salva para Local '{local_selecionado}' e Serviço '{servico_selecionado}'.")

# --- Mostrar tabela atualizada ---
st.write("Dados atuais da planilha:")
st.dataframe(df)

# --- Botão exportar ---
if st.button("Exportar para Excel"):

    nome_export = os.path.join(DATA_DIR, "medicao_exportada.xlsx")
    df.to_excel(nome_export, index=False)
    st.success(f"Arquivo exportado: {nome_export}")
    st.write(f"Baixe a planilha exportada em: {nome_export} (no servidor)")

