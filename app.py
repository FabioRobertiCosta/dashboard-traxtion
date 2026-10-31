import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página para tela cheia
st.set_page_config(page_title="Traxtion - Dashboard de Demanda", layout="wide")

# Título Principal
st.title("🚂 Traxtion - Dashboard Executivo de Demanda")
st.markdown("**Análise de SKUs, Categorias e Ordens de Compra (Frota de 100 Locomotivas)**")

# Carregar os dados da aba correta do Excel executivo
@st.cache_data
def load_data():
    try:
        return pd.read_excel('Traxtion_Demanda_Executivo.xlsx', sheet_name='Base de Dados')
    except:
        return pd.read_excel('data/Traxtion_Demanda_Executivo.xlsx', sheet_name='Base de Dados')

df = load_data()

# Filtro lateral mais amigável com Checkboxes organizados
st.sidebar.header("🔍 Filtros por Categoria")
st.sidebar.markdown("Selecione abaixo as categorias desejadas:")

# Obter categorias únicas ordenadas
categorias_disponiveis = sorted(df['Category'].dropna().unique())

# Criar um dicionário para armazenar o estado dos checkboxes
categorias_selecionadas = []
select_all = st.sidebar.checkbox("Selecionar Todas", value=True)

st.sidebar.markdown("---")

for cat in categorias_disponiveis:
    # Se "Selecionar Todas" estiver marcado, por padrão marca todas; caso contrário, usa o checkbox individual
    ativo = st.sidebar.checkbox(f"Categoria: {cat}", value=select_all, key=f"cat_{cat}")
    if ativo:
        categorias_selecionadas.append(cat)

# Filtrar o DataFrame com base na seleção
df_filtered = df[df['Category'].isin(categorias_selecionadas)]

# KPIs Principais
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de SKUs", f"{len(df_filtered):,}")
with col2:
    st.metric("Volume Total de Peças", f"{df_filtered['Total_Quantity'].sum():,}")
with col3:
    st.metric("Total de POs (Ordens)", f"{df_filtered['Total_POs'].sum():,}")
with col4:
    st.metric("Categorias Ativas", f"{len(categorias_selecionadas)}")

st.markdown("---")

# Gráficos Lado a Lado
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📦 Top 10 Itens por Quantidade Total")
    if not df_filtered.empty:
        top_items = df_filtered.nlargest(10, 'Total_Quantity')
        fig_top = px.bar(
            top_items, 
            x='Total_Quantity', 
            y='Description Item', 
            orientation='h',
            text='Total_Quantity',
            color='Category'
        )
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.warning("Nenhum dado selecionado para exibir no gráfico.")

with col_right:
    st.subheader("📊 Distribuição por Categoria")
    if not df_filtered.empty:
        cat_summary = df_filtered.groupby('Category')['Total_Quantity'].sum().reset_index()
        fig_pie = px.pie(
            cat_summary, 
            values='Total_Quantity', 
            names='Category', 
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Nenhum dado selecionado para exibir no gráfico.")

# Tabela Detalhada
st.subheader("📋 Base de Dados Consolidada")
st.dataframe(df_filtered, use_container_width=True)