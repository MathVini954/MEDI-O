import streamlit as st
import pandas as pd
from io import BytesIO

# Função para baixar Excel no Streamlit
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Medições')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

st.title('App de Medição de Obra - Mensal')

# Lê a planilha base
try:
    base_df = pd.read_excel('medicao_base.xlsx')
except Exception as e:
    st.error(f'Erro ao ler a planilha base: {e}')
    st.stop()

st.write('Planilha base carregada com sucesso!')
st.write(base_df)

# Criar colunas para digitar medição para cada linha da planilha base
st.header('Informe a medição mensal para cada serviço e local')

medicoes = []

for idx, row in base_df.iterrows():
    st.write(f"**Local:** {row['Local']} - **Serviço:** {row['Serviço']} - **Unidade:** {row['Unidade']}")
    valor = st.number_input(f'Medição ({row["Unidade"]})', min_value=0.0, format="%.2f", key=f'med_{idx}')
    medicoes.append(valor)

# Botão para exportar
if st.button('Exportar medições para Excel'):
    df_export = base_df.copy()
    df_export['Medição'] = medicoes

    excel_data = to_excel(df_export)

    st.download_button(
        label="Clique para baixar o arquivo Excel",
        data=excel_data,
        file_name='medicoes_mes.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
