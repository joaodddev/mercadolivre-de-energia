import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Mercado Livre de Energia",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para estilo moderno
st.markdown("""
<style>
    /* Estilo global */
    .main {
        background-color: #f5f7fb;
    }
    
    /* Cards modernos */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(0, 0, 0, 0.04);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.04);
    }
    
    /* Títulos das métricas */
    .metric-label {
        font-size: 0.85rem;
        color: #5f6c84;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a2639;
        margin-top: 8px;
    }
    .metric-delta {
        font-size: 0.85rem;
        color: #2ecc71;
        margin-top: 4px;
    }
    
    /* Header */
    .dashboard-header {
        background: linear-gradient(90deg, #1a2639 0%, #2c3e50 100%);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 25px;
        color: white;
    }
    
    /* Filtros */
    .filter-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid rgba(0, 0, 0, 0.04);
    }
    
    /* Cards de gráficos */
    .chart-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(0, 0, 0, 0.04);
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a2639;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
    }
    
    /* Tabela */
    .dataframe-container {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(0, 0, 0, 0.04);
    }
</style>
""", unsafe_allow_html=True)

# Header moderno
st.markdown("""
<div class="dashboard-header">
    <h1 style='margin:0; font-size: 2.2rem; font-weight: 700;'>⚡ Mercado Livre de Energia</h1>
    <p style='margin:10px 0 0 0; opacity:0.9; font-size: 1.1rem;'>Transformando dados em insights estratégicos</p>
</div>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("energia (1).csv", parse_dates=["data"])
    df["custo_livre"] = df["consumo_mwh"] * df["preco_contratado_mwh"]
    df["custo_cativo"] = df["consumo_mwh"] * df["preco_cativo_mwh"]
    df["economia"] = df["custo_cativo"] - df["custo_livre"]
    df["mes"] = df["data"].dt.strftime("%b/%Y")
    df["ano_mes"] = df["data"].dt.strftime("%Y-%m")
    return df

df = load_data()

# Container de filtros
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col_filtros1, col_filtros2, col_filtros3 = st.columns([1.5, 1.5, 1])

with col_filtros1:
    # Date filter
    min_date_df = df['data'].min()
    max_date_df = df['data'].max()
    
    start_date, end_date = st.date_input(
        "📅 Período de Análise",
        value=(min_date_df, max_date_df),
        min_value=min_date_df,
        max_value=max_date_df,
        format="DD/MM/YYYY"
    )

with col_filtros2:
    # Filter DataFrame by selected date range
    df_date_filtered = df[(df['data'] >= pd.to_datetime(start_date)) & 
                          (df['data'] <= pd.to_datetime(end_date))]
    
    # Unidade filter
    unidades_disponiveis = df_date_filtered["unidade"].unique()
    unidade = st.multiselect(
        "🏭 Unidades",
        unidades_disponiveis,
        default=unidades_disponiveis
    )

with col_filtros3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Limpar Filtros", use_container_width=True):
        start_date = min_date_df
        end_date = max_date_df
        unidade = unidades_disponiveis

st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtro = df_date_filtered[df_date_filtered["unidade"].isin(unidade)]

# Cálculos para KPIs
consumo_total = df_filtro['consumo_mwh'].sum()
custo_livre_total = df_filtro['custo_livre'].sum()
custo_cativo_total = df_filtro['custo_cativo'].sum()
economia_total = df_filtro['economia'].sum()
preco_medio_ponderado = (custo_livre_total + custo_cativo_total) / consumo_total if consumo_total > 0 else 0

# KPIs em cards modernos
st.markdown("## 📊 Indicadores de Performance")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ Consumo Total</div>
        <div class="metric-value">{consumo_total:,.0f}</div>
        <div class="metric-delta">MWh</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    economia_percentual = (economia_total / custo_cativo_total * 100) if custo_cativo_total > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 Economia Total</div>
        <div class="metric-value">R$ {economia_total:,.0f}</div>
        <div class="metric-delta">▼ {economia_percentual:.1f}% vs. Cativo</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏭 Mercado Livre</div>
        <div class="metric-value">R$ {custo_livre_total:,.0f}</div>
        <div class="metric-delta">R$ {df_filtro['preco_contratado_mwh'].mean():.2f}/MWh médio</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚙️ Mercado Cativo</div>
        <div class="metric-value">R$ {custo_cativo_total:,.0f}</div>
        <div class="metric-delta">R$ {df_filtro['preco_cativo_mwh'].mean():.2f}/MWh médio</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📉 Preço Médio</div>
        <div class="metric-value">R$ {preco_medio_ponderado:,.2f}</div>
        <div class="metric-delta">/MWh ponderado</div>
    </div>
    """, unsafe_allow_html=True)

# Gráficos
st.markdown("<br>", unsafe_allow_html=True)

# Linha 1: Evolução e Comparativo
col_esq, col_dir = st.columns([1.2, 0.8])

with col_esq:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Evolução Mensal - Custos & Economia</div>', unsafe_allow_html=True)
    
    # Preparar dados para o gráfico de evolução
    df_evolucao = df_filtro.groupby("data").agg({
        "custo_livre": "sum",
        "custo_cativo": "sum",
        "economia": "sum"
    }).reset_index()
    
    fig_evolucao = go.Figure()
    
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao["data"],
        y=df_evolucao["custo_cativo"],
        name="Mercado Cativo",
        line=dict(color="#e74c3c", width=3),
        fill=None
    ))
    
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao["data"],
        y=df_evolucao["custo_livre"],
        name="Mercado Livre",
        line=dict(color="#27ae60", width=3),
        fill=None
    ))
    
    fig_evolucao.add_trace(go.Bar(
        x=df_evolucao["data"],
        y=df_evolucao["economia"],
        name="Economia (R$)",
        marker_color="#3498db",
        opacity=0.7,
        yaxis="y2"
    ))
    
    fig_evolucao.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title="",
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            title="Custo (R$)",
            gridcolor='rgba(0,0,0,0.05)',
            title_font=dict(size=12)
        ),
        yaxis2=dict(
            title="Economia (R$)",
            overlaying="y",
            side="right",
            showgrid=False,
            title_font=dict(size=12, color="#3498db")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig_evolucao, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_dir:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">⚡ Consumo por Unidade</div>', unsafe_allow_html=True)
    
    # Gráfico de rosca para consumo
    df_consumo_unidade = df_filtro.groupby("unidade")["consumo_mwh"].sum().reset_index()
    
    fig_rosca = go.Figure(data=[go.Pie(
        labels=df_consumo_unidade["unidade"],
        values=df_consumo_unidade["consumo_mwh"],
        hole=.6,
        marker=dict(colors=['#2ecc71', '#3498db', '#e74c3c', '#f39c12']),
        textinfo='label+percent',
        textposition='outside',
        showlegend=False
    )])
    
    fig_rosca.update_layout(
        height=400,
        annotations=[dict(
            text=f'{consumo_total:,.0f}<br>MWh',
            x=0.5, y=0.5,
            font_size=20,
            font_weight='bold',
            showarrow=False
        )],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_rosca, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Linha 2: Análise de Preços e Economia Acumulada
col_precos, col_acumulada = st.columns(2)

with col_precos:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💰 Comparativo de Preços (R$/MWh)</div>', unsafe_allow_html=True)
    
    # Preparar dados para gráfico de preços
    df_precos = df_filtro.groupby(["data", "unidade"]).agg({
        "preco_contratado_mwh": "mean",
        "preco_cativo_mwh": "mean"
    }).reset_index()
    
    fig_precos = go.Figure()
    
    for unidade in df_precos["unidade"].unique():
        df_unidade = df_precos[df_precos["unidade"] == unidade]
        fig_precos.add_trace(go.Scatter(
            x=df_unidade["data"],
            y=df_unidade["preco_contratado_mwh"],
            name=f"{unidade} - Livre",
            line=dict(dash='solid'),
            mode='lines+markers'
        ))
    
    # Adicionar linha do preço cativo (constante por período)
    preco_cativo_medio = df_filtro.groupby("data")["preco_cativo_mwh"].mean()
    
    fig_precos.add_trace(go.Scatter(
        x=preco_cativo_medio.index,
        y=preco_cativo_medio.values,
        name="Mercado Cativo",
        line=dict(color="red", width=3, dash='dash'),
        mode='lines'
    ))
    
    fig_precos.update_layout(
        height=350,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig_precos, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_acumulada:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Economia Acumulada por Unidade</div>', unsafe_allow_html=True)
    
    # Calcular economia acumulada por unidade
    df_acumulado = df_filtro.copy()
    df_acumulado = df_acumulado.sort_values(['unidade', 'data'])
    df_acumulado['economia_acumulada'] = df_acumulado.groupby('unidade')['economia'].cumsum()
    
    fig_acumulado = px.area(
        df_acumulado,
        x='data',
        y='economia_acumulada',
        color='unidade',
        line_group='unidade',
        color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    )
    
    fig_acumulado.update_layout(
        height=350,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)', title="Economia Acumulada (R$)")
    )
    
    st.plotly_chart(fig_acumulado, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tabela de detalhamento
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">📋 Detalhamento dos Dados</div>', unsafe_allow_html=True)

# Formatar dados para exibição
df_display = df_filtro.copy()
df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
df_display['consumo_mwh'] = df_display['consumo_mwh'].apply(lambda x: f"{x:,.0f}")
df_display['preco_contratado_mwh'] = df_display['preco_contratado_mwh'].apply(lambda x: f"R$ {x:,.2f}")
df_display['preco_cativo_mwh'] = df_display['preco_cativo_mwh'].apply(lambda x: f"R$ {x:,.2f}")
df_display['custo_livre'] = df_display['custo_livre'].apply(lambda x: f"R$ {x:,.2f}")
df_display['custo_cativo'] = df_display['custo_cativo'].apply(lambda x: f"R$ {x:,.2f}")
df_display['economia'] = df_display['economia'].apply(lambda x: f"R$ {x:,.2f}")

# Renomear colunas para português
df_display.columns = ['Data', 'Unidade', 'Consumo (MWh)', 'Preço Livre (R$/MWh)', 
                      'Preço Cativo (R$/MWh)', 'Custo Livre (R$)', 'Custo Cativo (R$)', 
                      'Economia (R$)', 'Mês', 'Ano/Mês']

st.dataframe(
    df_display.drop(['Mês', 'Ano/Mês'], axis=1),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Data": st.column_config.TextColumn("Data", width="small"),
        "Unidade": st.column_config.TextColumn("Unidade", width="small"),
        "Consumo (MWh)": st.column_config.TextColumn("Consumo (MWh)", width="small"),
        "Preço Livre (R$/MWh)": st.column_config.TextColumn("Preço Livre (R$/MWh)", width="medium"),
        "Preço Cativo (R$/MWh)": st.column_config.TextColumn("Preço Cativo (R$/MWh)", width="medium"),
        "Custo Livre (R$)": st.column_config.TextColumn("Custo Livre (R$)", width="medium"),
        "Custo Cativo (R$)": st.column_config.TextColumn("Custo Cativo (R$)", width="medium"),
        "Economia (R$)": st.column_config.TextColumn("Economia (R$)", width="medium"),
    }
)

# Rodapé com insights
st.markdown("<br>", unsafe_allow_html=True)
col_insight1, col_insight2, col_insight3 = st.columns(3)

with col_insight1:
    economia_periodo = df_filtro['economia'].sum()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px;'>
        <p style='color: white; opacity: 0.9; margin:0; font-size: 0.9rem;'>💡 INSIGHT</p>
        <p style='color: white; margin:10px 0 0 0; font-size: 1rem;'>Economia total no período: <strong>R$ {economia_periodo:,.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    melhor_unidade = df_filtro.groupby('unidade')['economia'].sum().idxmax()
    melhor_economia = df_filtro.groupby('unidade')['economia'].sum().max()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 20px; border-radius: 12px;'>
        <p style='color: white; opacity: 0.9; margin:0; font-size: 0.9rem;'>🏆 DESTAQUE</p>
        <p style='color: white; margin:10px 0 0 0; font-size: 1rem;'>{melhor_unidade} - Economia: <strong>R$ {melhor_economia:,.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
    economia_media_mensal = df_filtro.groupby('data')['economia'].sum().mean()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px;'>
        <p style='color: white; opacity: 0.9; margin:0; font-size: 0.9rem;'>📊 MÉDIA MENSAL</p>
        <p style='color: white; margin:10px 0 0 0; font-size: 1rem;'>Economia média: <strong>R$ {economia_media_mensal:,.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)
