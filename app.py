
import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Mercado Livre de Energia",
    layout="wide"
)

st.title("💡 Transformando Dados em Insights - Mercado Livre de Energia")

# Carregar dados
df = pd.read_csv("energia.csv", parse_dates=["data"])

# Cálculos
df["custo_livre"] = df["consumo_mwh"] * df["preco_contratado_mwh"]
df["custo_cativo"] = df["consumo_mwh"] * df["preco_cativo_mwh"]
df["economia"] = df["custo_cativo"] - df["custo_livre"]

# Determine min and max dates for the date filter
min_date_df = df['data'].min()
max_date_df = df['data'].max()

# Date filter
start_date, end_date = st.date_input(
    "Selecione o período:",
    value=(min_date_df, max_date_df),
    min_value=min_date_df,
    max_value=max_date_df
)

# Filter DataFrame by selected date range
df_date_filtered = df[(df['data'] >= pd.to_datetime(start_date)) & (df['data'] <= pd.to_datetime(end_date))]

# Filters
unidade = st.multiselect(
    "Selecione a unidade:",
    df_date_filtered["unidade"].unique(),
    default=df_date_filtered["unidade"].unique()
)

# Update df_filtro to use df_date_filtered
df_filtro = df_date_filtered[df_date_filtered["unidade"].isin(unidade)]

# Calculate new KPIs
preco_medio_ponderado_total = (df_filtro['custo_livre'].sum() + df_filtro['custo_cativo'].sum()) / df_filtro['consumo_mwh'].sum()
economia_acumulada_kpi = df_filtro['economia'].sum()

# KPIs
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Consumo Total (MWh)", f"{df_filtro['consumo_mwh'].sum():,.0f}")
col2.metric("Custo Mercado Livre (R$)", f"{df_filtro['custo_livre'].sum():,.0f}")
col3.metric("Custo Mercado Cativo (R$)", f"{df_filtro['custo_cativo'].sum():,.0f}")
col4.metric("Economia Total (R$)", f"{df_filtro['economia'].sum():,.0f}")
col5.metric("Preço Médio Ponderado (R$/MWh)", f"{preco_medio_ponderado_total:,.2f}")
col6.metric("Economia Acumulada (R$)", f"{economia_acumulada_kpi:,.0f}")

# Gráficos
st.subheader("📈 Evolução Mensal")

# Prepare data for 'Evolução Mensal' chart
df_chart_evolucao = df_filtro.copy()
df_chart_evolucao = df_chart_evolucao.sort_values(by=['unidade', 'data'])
df_chart_evolucao['economia_acumulada'] = df_chart_evolucao.groupby('unidade')['economia'].cumsum()

df_grouped_for_chart = df_chart_evolucao.groupby("data")[["custo_livre", "custo_cativo", "economia_acumulada"]].sum()

st.line_chart(
    df_grouped_for_chart
)

st.subheader("⚡ Consumo por Unidade")

st.bar_chart(
    df_filtro.groupby("unidade")["consumo_mwh"].sum()
)

# Tabela
st.subheader("📋 Detalhamento dos Dados")
st.dataframe(df_filtro)
