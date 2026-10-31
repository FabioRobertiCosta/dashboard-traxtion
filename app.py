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
    # Base de dados simulada e rica para exibição perfeita na nuvem (Cloud)
    dados_mock = {
        "Cliente": [
            "Empresa A",
            "Empresa B",
            "Empresa C",
            "Empresa D",
            "Empresa E",
        ],
        "Status": [
            "Concluído",
            "Em Andamento",
            "Pendente",
            "Concluído",
            "Em Andamento",
        ],
        "Demanda": [120, 85, 45, 200, 95],
        "Valor": [15000, 9500, 4300, 25000, 11000],
    }
    return pd.DataFrame(dados_mock)


# Carregando os dados
df = load_data()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🔍 Filtros do Dashboard")

# Filtro de Status (se a coluna existir)
if "Status" in df.columns:
  status_disponiveis = df["Status"].unique().tolist()
  status_selecionados = st.sidebar.multiselect(
      "Selecione o Status",
      options=status_disponiveis,
      default=status_disponiveis,
  )
  if status_selecionados:
    df = df[df["Status"].isin(status_selecionados)]

# Filtro de Cliente (se a coluna existir)
if "Cliente" in df.columns:
  clientes_disponiveis = df["Cliente"].unique().tolist()
  clientes_selecionados = st.sidebar.multiselect(
      "Selecione o Cliente",
      options=clientes_disponiveis,
      default=clientes_disponiveis,
  )
  if clientes_selecionados:
    df = df[df["Cliente"].isin(clientes_selecionados)]

# --- TÍTULO PRINCIPAL ---
st.title("📊 Traxtion - Dashboard Executivo de Demandas")
st.markdown(
    "Painel interativo para acompanhamento de demandas e métricas estratégicas."
)

# --- MÉTRICAS EXECUTIVAS ---
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
  if "Demanda" in df.columns:
    st.metric(
        label="Demanda Total",
        value=f"{df['Demanda'].sum():,.0f}".replace(",", "."),
    )
  else:
    st.metric(label="Ambiente", value="Produção (Cloud)")

st.divider()

# --- SEÇÃO DE GRÁFICOS (VISUALIZAÇÃO) ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
  st.subheader("📈 Demandas por Cliente")
  if "Cliente" in df.columns and "Demanda" in df.columns:
    fig_bar = px.bar(
        df,
        x="Cliente",
        y="Demanda",
        color="Status" if "Status" in df.columns else None,
        title="Volume de Demanda por Cliente",
        template="plotly_dark",
    )
    st.plotly_chart(fig_bar, use_container_width=True)
  else:
    st.warning("Colunas necessárias não encontradas para o gráfico de barras.")

with col_graf2:
  st.subheader("🥧 Distribuição por Status")
  if "Status" in df.columns and "Demanda" in df.columns:
    fig_pie = px.pie(
        df,
        names="Status",
        values="Demanda",
        title="Participação por Status de Demanda",
        template="plotly_dark",
        hole=0.4,  # Estilo Donut Chart elegante
    )
    st.plotly_chart(fig_pie, use_container_width=True)
  else:
    st.warning("Colunas necessárias não encontradas para o gráfico de pizza.")

st.divider()

# --- TABELA DE DADOS ---
st.subheader("📋 Tabela de Dados Detalhados")
st.dataframe(df, use_container_width=True)