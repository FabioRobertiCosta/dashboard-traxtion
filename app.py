import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Traxtion - Dashboard de Demanda",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
  caminho_arquivo = "data/Traxtion_Demanda_Executivo.xlsx"

  # Verifica se o arquivo Excel existe localmente
  if os.path.exists(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo, sheet_name="Base de Dados")
    return df
  else:
    # Base de dados simulada para exibição segura na nuvem (Cloud)
    dados_mock = {
        "Cliente": ["Empresa A", "Empresa B", "Empresa C", "Empresa D"],
        "Status": ["Concluído", "Em Andamento", "Pendente", "Concluído"],
        "Demanda": [120, 85, 45, 200],
        "Valor": [15000, 9500, 4300, 25000],
    }
    return pd.DataFrame(dados_mock)


# Carregando os dados
df = load_data()

st.title("📊 Traxtion - Dashboard Executivo de Demandas")
st.markdown(
    "Painel interativo para acompanhamento de demandas e métricas estratégicas."
)

# Exibição de métricas rápidas
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(
      label="Total de Registros", value=f"{df.shape[0]:,.0f}".replace(",", ".")
  )
with col2:
  if "Valor" in df.columns:
    st.metric(
        label="Valor Total",
        value=f"R$ {df['Valor'].sum():,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )
  else:
    st.metric(label="Métrica Secundária", value="Ativo")
with col3:
  st.metric(label="Ambiente", value="Produção (Cloud)")

st.divider()

# Gráfico de Exemplo com Plotly
st.subheader("📈 Análise Visual de Demandas")
if "Cliente" in df.columns and "Demanda" in df.columns:
  fig = px.bar(
      df,
      x="Cliente",
      y="Demanda",
      color="Status" if "Status" in df.columns else None,
      title="Demandas por Cliente",
      template="plotly_dark",
  )
  st.plotly_chart(fig, use_container_width=True)
else:
  st.warning("As colunas esperadas não foram encontradas no conjunto de dados.")

# Exibição da tabela detalhada
st.subheader("📋 Tabela de Dados Detalhados")
st.dataframe(df, use_container_width=True)