import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Mercado Livre de Energia • Dark Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para estilo DEEP DARK ANALYTICS
st.markdown("""
<style>
    /* Dark theme global */
    .stApp {
        background: linear-gradient(135deg, #0a0c0f 0%, #1a1e24 100%);
        color: #e0e0e0;
    }
    
    /* Cards com efeito glassmorphism dark */
    .metric-card {
        background: rgba(18, 22, 28, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(46, 204, 113, 0.15);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #2ecc71, #3498db, #9b59b6);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(46, 204, 113, 0.4);
        box-shadow: 0 12px 48px rgba(46, 204, 113, 0.15);
        background: rgba(26, 32, 44, 0.95);
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #8892b0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 4px;
        text-shadow: 0 0 20px rgba(46, 204, 113, 0.3);
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #2ecc71;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    /* Header Dark */
    .dashboard-header {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(46, 204, 113, 0.2);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(46, 204, 113, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    
    /* Filtros Dark */
    .filter-container {
        background: rgba(18, 22, 28, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(46, 204, 113, 0.15);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 28px;
    }
    
    /* Cards de gráficos */
    .chart-card {
        background: rgba(18, 22, 28, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(46, 204, 113, 0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.5px;
        text-shadow: 0 0 15px rgba(46, 204, 113, 0.3);
    }
    
    /* Tabela Dark */
    .dataframe-container {
        background: rgba(18, 22, 28, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(46, 204, 113, 0.15);
        border-radius: 20px;
        padding: 24px;
    }
    
    /* Customização de elementos Streamlit */
    .stSelectbox, .stMultiSelect, .stDateInput {
        background-color: rgba(26, 32, 44, 0.8) !important;
        border-color: rgba(46, 204, 113, 0.2) !important;
        color: white !important;
    }
    
    .st-bb, .st-at {
        background-color: #1a1e24 !important;
        color: white !important;
    }
    
    /* Botão Dark */
    .stButton > button {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 16px rgba(46, 204, 113, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(46, 204, 113, 0.5) !important;
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0c0f;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2ecc71;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #27ae60;
    }
    
    /* Texto e links */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #e0e0e0 !important;
    }
    
    /* Cards de insight dark */
    .insight-card {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(52, 152, 219, 0.1) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(46, 204, 113, 0.2);
        border-radius: 16px;
        padding: 24px;
    }
</style>

<script>
    // Adiciona classe dark ao body
    document.body.classList.add('dark-theme');
</script>
""", unsafe_allow_html=True)

# Header Dark Analytics
st.markdown("""
<div class="dashboard-header">
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='margin:0; font-size: 2.4rem; font-weight: 700; background: linear-gradient(135deg, #2ecc71, #3498db); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;'>
                ⚡ DEEP DARK ANALYTICS
            </h1>
            <p style='margin:12px 0 0 0; color: #8892b0; font-size: 1.1rem; letter-spacing: 1px;'>Mercado Livre de Energia • Intelligence Platform</p>
        </div>
        <div style='background: rgba(46, 204, 113, 0.1); padding: 12px 24px; border-radius: 30px; border: 1px solid rgba(46, 204, 113, 0.2);'>
            <span style='color: #2ecc71; font-size: 0.9rem;'>🟢 LIVE DASHBOARD</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Carregar dados com cache
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv("energia.csv", parse_dates=["data"])
    df["custo_livre"] = df["consumo_mwh"] * df["preco_contratado_mwh"]
    df["custo_cativo"] = df["consumo_mwh"] * df["preco_cativo_mwh"]
    df["economia"] = df["custo_cativo"] - df["custo_livre"]
    df["mes"] = df["data"].dt.strftime("%b/%Y")
    df["ano_mes"] = df["data"].dt.strftime("%Y-%m")
    df["economia_percentual"] = (df["economia"] / df["custo_cativo"] * 100).round(1)
    return df

df = load_data()

# Filtros Dark
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col_filtros1, col_filtros2, col_filtros3 = st.columns([1.5, 1.5, 1])

with col_filtros1:
    min_date_df = df['data'].min()
    max_date_df = df['data'].max()
    
    start_date, end_date = st.date_input(
        "📅 PERÍODO DE ANÁLISE",
        value=(min_date_df, max_date_df),
        min_value=min_date_df,
        max_value=max_date_df,
        format="DD/MM/YYYY"
    )

with col_filtros2:
    df_date_filtered = df[(df['data'] >= pd.to_datetime(start_date)) & 
                          (df['data'] <= pd.to_datetime(end_date))]
    
    unidades_disponiveis = df_date_filtered["unidade"].unique()
    unidade = st.multiselect(
        "🏭 UNIDADES",
        unidades_disponiveis,
        default=unidades_disponiveis
    )

with col_filtros3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 LIMPAR FILTROS", use_container_width=True):
        start_date = min_date_df
        end_date = max_date_df
        unidade = unidades_disponiveis

st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtro = df_date_filtered[df_date_filtered["unidade"].isin(unidade)]

# Cálculos avançados
consumo_total = df_filtro['consumo_mwh'].sum()
custo_livre_total = df_filtro['custo_livre'].sum()
custo_cativo_total = df_filtro['custo_cativo'].sum()
economia_total = df_filtro['economia'].sum()
preco_medio_ponderado = (custo_livre_total + custo_cativo_total) / consumo_total if consumo_total > 0 else 0
economia_percentual_media = df_filtro['economia_percentual'].mean()
ticket_medio_livre = custo_livre_total / consumo_total if consumo_total > 0 else 0

# KPIs Dark Analytics
st.markdown("## 📊 DASHBOARD DE PERFORMANCE")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚡ TOTAL CONSUMO</div>
        <div class="metric-value">{consumo_total:,.0f}</div>
        <div class="metric-delta">
            <span style='color: #2ecc71;'>●</span> {len(df_filtro['data'].unique())} períodos
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    economia_vs_cativo = (economia_total / custo_cativo_total * 100) if custo_cativo_total > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 ECONOMIA TOTAL</div>
        <div class="metric-value" style='color: #2ecc71;'>R$ {economia_total:,.0f}</div>
        <div class="metric-delta">
            <span style='color: #2ecc71;'>▼</span> {economia_vs_cativo:.1f}% vs Cativo
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏭 MERCADO LIVRE</div>
        <div class="metric-value">R$ {custo_livre_total:,.0f}</div>
        <div class="metric-delta">
            <span style='color: #3498db;'>●</span> R$ {df_filtro['preco_contratado_mwh'].mean():.2f}/MWh
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⚙️ MERCADO CATIVO</div>
        <div class="metric-value">R$ {custo_cativo_total:,.0f}</div>
        <div class="metric-delta">
            <span style='color: #e74c3c;'>●</span> R$ {df_filtro['preco_cativo_mwh'].mean():.2f}/MWh
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📉 PREÇO MÉDIO</div>
        <div class="metric-value">R$ {preco_medio_ponderado:,.2f}</div>
        <div class="metric-delta">
            <span style='color: #9b59b6;'>●</span> /MWh ponderado
        </div>
    </div>
    """, unsafe_allow_html=True)

# Gráficos Dark Analytics
st.markdown("<br>", unsafe_allow_html=True)

# Linha 1: Gráficos principais
col_esq, col_dir = st.columns([1.2, 0.8])

with col_esq:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 EVOLUÇÃO TEMPORAL • CUSTOS & ECONOMIA</div>', unsafe_allow_html=True)
    
    df_evolucao = df_filtro.groupby("data").agg({
        "custo_livre": "sum",
        "custo_cativo": "sum",
        "economia": "sum"
    }).reset_index()
    
    fig_evolucao = go.Figure()
    
    # Adicionar áreas com gradiente
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao["data"],
        y=df_evolucao["custo_cativo"],
        name="Mercado Cativo",
        line=dict(color="#e74c3c", width=2.5),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    fig_evolucao.add_trace(go.Scatter(
        x=df_evolucao["data"],
        y=df_evolucao["custo_livre"],
        name="Mercado Livre",
        line=dict(color="#2ecc71", width=2.5),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.1)'
    ))
    
    fig_evolucao.add_trace(go.Bar(
        x=df_evolucao["data"],
        y=df_evolucao["economia"],
        name="Economia (R$)",
        marker_color="#3498db",
        opacity=0.8,
        yaxis="y2"
    ))
    
    fig_evolucao.update_layout(
        height=450,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8892b0'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title="Custo (R$)",
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            title_font=dict(color='white')
        ),
        yaxis2=dict(
            title="Economia (R$)",
            overlaying="y",
            side="right",
            gridcolor='rgba(255,255,255,0.05)',
            title_font=dict(color='#3498db')
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig_evolucao, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_dir:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">⚡ DISTRIBUIÇÃO DE CONSUMO</div>', unsafe_allow_html=True)
    
    df_consumo_unidade = df_filtro.groupby("unidade")["consumo_mwh"].sum().reset_index()
    
    fig_rosca = go.Figure(data=[go.Pie(
        labels=df_consumo_unidade["unidade"],
        values=df_consumo_unidade["consumo_mwh"],
        hole=.65,
        marker=dict(
            colors=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
            line=dict(color='#1a1e24', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(color='white'),
        showlegend=False,
        hoverinfo='label+value+percent'
    )])
    
    fig_rosca.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(
            text=f'{consumo_total:,.0f}<br>MWh',
            x=0.5, y=0.5,
            font_size=22,
            font_weight='bold',
            font_color='white',
            showarrow=False
        )],
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_rosca, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Linha 2: Análise de Preços e Economia
col_precos, col_acumulada = st.columns(2)

with col_precos:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💰 COMPARATIVO DE PREÇOS • R$/MWh</div>', unsafe_allow_html=True)
    
    df_precos = df_filtro.groupby(["data", "unidade"]).agg({
        "preco_contratado_mwh": "mean",
        "preco_cativo_mwh": "mean"
    }).reset_index()
    
    fig_precos = go.Figure()
    
    cores = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    for i, unidade in enumerate(df_precos["unidade"].unique()):
        df_unidade = df_precos[df_precos["unidade"] == unidade]
        fig_precos.add_trace(go.Scatter(
            x=df_unidade["data"],
            y=df_unidade["preco_contratado_mwh"],
            name=f"{unidade} - Livre",
            line=dict(color=cores[i % len(cores)], width=2),
            mode='lines+markers',
            marker=dict(size=8)
        ))
    
    preco_cativo_medio = df_filtro.groupby("data")["preco_cativo_mwh"].mean()
    
    fig_precos.add_trace(go.Scatter(
        x=preco_cativo_medio.index,
        y=preco_cativo_medio.values,
        name="Mercado Cativo",
        line=dict(color="#e74c3c", width=3, dash='dash'),
        mode='lines'
    ))
    
    fig_precos.update_layout(
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8892b0'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig_precos, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_acumulada:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 ECONOMIA ACUMULADA • POR UNIDADE</div>', unsafe_allow_html=True)
    
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
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8892b0'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.1)',
            title="Economia Acumulada (R$)"
        ),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig_acumulado, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tabela Dark
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">📋 DATAFRAME ANALYTICS • DADOS DETALHADOS</div>', unsafe_allow_html=True)

# Formatar dados
df_display = df_filtro.copy()
df_display['data'] = df_display['data'].dt.strftime('%Y-%m-%d')
df_display['consumo_mwh'] = df_display['consumo_mwh'].apply(lambda x: f"{x:,.0f}")
df_display['preco_contratado_mwh'] = df_display['preco_contratado_mwh'].apply(lambda x: f"R$ {x:,.2f}")
df_display['preco_cativo_mwh'] = df_display['preco_cativo_mwh'].apply(lambda x: f"R$ {x:,.2f}")
df_display['custo_livre'] = df_display['custo_livre'].apply(lambda x: f"R$ {x:,.2f}")
df_display['custo_cativo'] = df_display['custo_cativo'].apply(lambda x: f"R$ {x:,.2f}")
df_display['economia'] = df_display['economia'].apply(lambda x: f"R$ {x:,.2f}")

df_display.columns = ['Data', 'Unidade', 'Consumo (MWh)', 'Preço Livre', 
                      'Preço Cativo', 'Custo Livre', 'Custo Cativo', 
                      'Economia', 'Mês', 'Ano/Mês', 'Economia %']

st.dataframe(
    df_display[['Data', 'Unidade', 'Consumo (MWh)', 'Preço Livre', 'Preço Cativo', 
                'Custo Livre', 'Custo Cativo', 'Economia', 'Economia %']],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Economia %": st.column_config.ProgressColumn(
            "Economia %",
            help="Percentual de economia em relação ao mercado cativo",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        )
    }
)
st.markdown('</div>', unsafe_allow_html=True)

# Insights Dark Analytics
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 🎯 INSIGHTS ESTRATÉGICOS")

col_insight1, col_insight2, col_insight3, col_insight4 = st.columns(4)

with col_insight1:
    economia_total_periodo = df_filtro['economia'].sum()
    st.markdown(f"""
    <div class="insight-card">
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='background: rgba(46, 204, 113, 0.2); padding: 12px; border-radius: 12px;'>
                <span style='color: #2ecc71; font-size: 1.5rem;'>💰</span>
            </div>
            <div>
                <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>ECONOMIA TOTAL</p>
                <p style='color: white; margin:4px 0 0 0; font-size: 1.3rem; font-weight: 700;'>R$ {economia_total_periodo:,.0f}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    melhor_unidade = df_filtro.groupby('unidade')['economia'].sum().idxmax()
    melhor_economia = df_filtro.groupby('unidade')['economia'].sum().max()
    st.markdown(f"""
    <div class="insight-card">
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='background: rgba(52, 152, 219, 0.2); padding: 12px; border-radius: 12px;'>
                <span style='color: #3498db; font-size: 1.5rem;'>🏆</span>
            </div>
            <div>
                <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>MELHOR PERFORMANCE</p>
                <p style='color: white; margin:4px 0 0 0; font-size: 1.1rem; font-weight: 600;'>{melhor_unidade}</p>
                <p style='color: #2ecc71; margin:0; font-size: 0.9rem;'>R$ {melhor_economia:,.0f}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
    economia_media_mensal = df_filtro.groupby('data')['economia'].sum().mean()
    st.markdown(f"""
    <div class="insight-card">
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='background: rgba(155, 89, 182, 0.2); padding: 12px; border-radius: 12px;'>
                <span style='color: #9b59b6; font-size: 1.5rem;'>📊</span>
            </div>
            <div>
                <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>MÉDIA MENSAL</p>
                <p style='color: white; margin:4px 0 0 0; font-size: 1.3rem; font-weight: 700;'>R$ {economia_media_mensal:,.0f}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight4:
    taxa_economia_media = df_filtro['economia_percentual'].mean()
    st.markdown(f"""
    <div class="insight-card">
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='background: rgba(241, 196, 15, 0.2); padding: 12px; border-radius: 12px;'>
                <span style='color: #f1c40f; font-size: 1.5rem;'>📉</span>
            </div>
            <div>
                <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>TAXA DE ECONOMIA</p>
                <p style='color: white; margin:4px 0 0 0; font-size: 1.3rem; font-weight: 700;'>{taxa_economia_media:.1f}%</p>
                <p style='color: #2ecc71; margin:0; font-size: 0.9rem;'>vs Mercado Cativo</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer Dark
st.markdown("""
<div style='margin-top: 48px; padding: 24px; border-top: 1px solid rgba(46, 204, 113, 0.2); text-align: center;'>
    <p style='color: #8892b0; font-size: 0.85rem; letter-spacing: 1px;'>
        ⚡ DEEP DARK ANALYTICS • MERCADO LIVRE DE ENERGIA • ÚLTIMA ATUALIZAÇÃO: 2026
    </p>
</div>
""", unsafe_allow_html=True)
