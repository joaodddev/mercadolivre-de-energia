import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Mercado Livre de Energia • Dark Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⚡"
)

# Custom CSS para DEEP DARK ANALYTICS com UX/UI avançado
st.markdown("""
<style>
    /* Dark theme global */
    .stApp {
        background: linear-gradient(135deg, #0a0c0f 0%, #1a1e24 100%);
        color: #e0e0e0;
    }
    
    /* ===== UX/UI IMPROVEMENTS ===== */
    
    /* Animated Background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Smooth Transitions */
    * {
        transition: all 0.2s ease-in-out;
    }
    
    /* Custom Tabs - UX Enhanced */
    .stTabs {
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(18, 22, 28, 0.6);
        backdrop-filter: blur(10px);
        padding: 12px;
        border-radius: 16px;
        border: 1px solid rgba(46, 204, 113, 0.15);
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        color: #8892b0 !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        border: 1px solid transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(46, 204, 113, 0.05) 100%) !important;
        border: 1px solid rgba(46, 204, 113, 0.3) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.1);
    }
    
    /* Cards com glassmorphism aprimorado */
    .metric-card, .chart-card, .filter-container {
        background: rgba(18, 22, 28, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(46, 204, 113, 0.15);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after, .chart-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(46, 204, 113, 0.05), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::after, .chart-card:hover::after {
        left: 100%;
    }
    
    /* Loading Animations */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .loading-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Tooltips Customizados */
    [data-tooltip] {
        position: relative;
        cursor: help;
    }
    
    [data-tooltip]:before {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 16px;
        background: rgba(26, 32, 44, 0.95);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 8px;
        color: white;
        font-size: 0.85rem;
        white-space: nowrap;
        z-index: 1000;
        opacity: 0;
        visibility: hidden;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    [data-tooltip]:hover:before {
        opacity: 1;
        visibility: visible;
        bottom: 120%;
    }
    
    /* Micro-interações */
    .clickable {
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .clickable:hover {
        transform: scale(1.02);
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .status-success {
        background: rgba(46, 204, 113, 0.15);
        border: 1px solid rgba(46, 204, 113, 0.3);
        color: #2ecc71;
    }
    
    .status-warning {
        background: rgba(241, 196, 15, 0.15);
        border: 1px solid rgba(241, 196, 15, 0.3);
        color: #f1c40f;
    }
    
    .status-info {
        background: rgba(52, 152, 219, 0.15);
        border: 1px solid rgba(52, 152, 219, 0.3);
        color: #3498db;
    }
    
    /* Progress Bar Custom */
    .custom-progress {
        width: 100%;
        height: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 12px;
    }
    
    .custom-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #2ecc71, #3498db);
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* Footer aprimorado */
    .dashboard-footer {
        margin-top: 48px;
        padding: 24px;
        border-top: 1px solid rgba(46, 204, 113, 0.2);
        text-align: center;
        position: relative;
    }
    
    .dashboard-footer::before {
        content: '';
        position: absolute;
        top: -1px;
        left: 10%;
        width: 80%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #2ecc71, #3498db, #2ecc71, transparent);
    }
</style>

<script>
    // Adiciona classe dark e detecta preferência de sistema
    document.body.classList.add('dark-theme');
    
    // Smooth scroll para navegação
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
</script>
""", unsafe_allow_html=True)

# Header com indicador de status
st.markdown("""
<div class="dashboard-header" style='background: rgba(0,0,0,0.3); backdrop-filter: blur(12px); border: 1px solid rgba(46,204,113,0.2); border-radius: 24px; padding: 28px; margin-bottom: 28px;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <div style='display: flex; align-items: center; gap: 16px; margin-bottom: 12px;'>
                <h1 style='margin:0; font-size: 2.4rem; font-weight: 700; background: linear-gradient(135deg, #2ecc71, #3498db); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;'>
                    ⚡ DEEP DARK ANALYTICS
                </h1>
                <span class='status-badge status-success' style='margin-left: 8px;'>● LIVE</span>
            </div>
            <p style='margin:0; color: #8892b0; font-size: 1.1rem; letter-spacing: 1px;'>Mercado Livre de Energia • Intelligence Platform</p>
        </div>
        <div style='display: flex; gap: 16px;'>
            <div class='status-badge status-info' data-tooltip='Última atualização dos dados'>
                📅 {datetime.now().strftime('%d/%m/%Y')}
            </div>
            <div class='status-badge status-success' data-tooltip='Status do sistema'>
                🟢 Sistema Operacional
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Carregar dados com cache
@st.cache_data(ttl=3600, show_spinner="🔄 Carregando dados energéticos...")
def load_data():
    df = pd.read_csv("energia.csv", parse_dates=["data"])
    df["custo_livre"] = df["consumo_mwh"] * df["preco_contratado_mwh"]
    df["custo_cativo"] = df["consumo_mwh"] * df["preco_cativo_mwh"]
    df["economia"] = df["custo_cativo"] - df["custo_livre"]
    df["mes"] = df["data"].dt.strftime("%b/%Y")
    df["ano_mes"] = df["data"].dt.strftime("%Y-%m")
    df["economia_percentual"] = (df["economia"] / df["custo_cativo"] * 100).round(1)
    df["eficiencia"] = (df["preco_contratado_mwh"] / df["preco_cativo_mwh"] * 100).round(1)
    return df

df = load_data()

# Filtros Globais com UX aprimorado
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
st.markdown("""
<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px;'>
    <span style='background: rgba(46,204,113,0.1); padding: 8px 16px; border-radius: 20px; border: 1px solid rgba(46,204,113,0.2);'>
        <span style='color: #2ecc71;'>🎯</span> 
        <span style='color: white; margin-left: 8px;'>FILTROS GLOBAIS</span>
    </span>
    <span style='color: #8892b0; font-size: 0.9rem;' data-tooltip='Os filtros afetam todas as abas do dashboard'>
        ⓘ
    </span>
</div>
""", unsafe_allow_html=True)

col_filtros1, col_filtros2, col_filtros3 = st.columns([1.5, 1.5, 1])

with col_filtros1:
    min_date_df = df['data'].min()
    max_date_df = df['data'].max()
    
    start_date, end_date = st.date_input(
        "📅 PERÍODO DE ANÁLISE",
        value=(min_date_df, max_date_df),
        min_value=min_date_df,
        max_value=max_date_df,
        format="DD/MM/YYYY",
        help="Selecione o intervalo de datas para análise"
    )

with col_filtros2:
    df_date_filtered = df[(df['data'] >= pd.to_datetime(start_date)) & 
                          (df['data'] <= pd.to_datetime(end_date))]
    
    unidades_disponiveis = df_date_filtered["unidade"].unique()
    unidade = st.multiselect(
        "🏭 UNIDADES",
        unidades_disponiveis,
        default=unidades_disponiveis,
        help="Selecione uma ou mais unidades para análise"
    )

with col_filtros3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 LIMPAR", use_container_width=True):
            start_date = min_date_df
            end_date = max_date_df
            unidade = unidades_disponiveis
    with col_btn2:
        if st.button("📥 EXPORTAR", use_container_width=True):
            st.session_state['export'] = True

st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtro = df_date_filtered[df_date_filtered["unidade"].isin(unidade)]

# ===== MÚLTIPLAS ABAS COM UX AVANÇADO =====
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 VISÃO GERAL",
    "💰 ANÁLISE FINANCEIRA", 
    "⚡ PERFORMANCE OPERACIONAL",
    "📈 PROJEÇÕES & TRENDS",
    "🔍 DADOS DETALHADOS"
])

# ===== TAB 1: VISÃO GERAL =====
with tab1:
    # KPIs Principais com micro-interações
    st.markdown("## 📊 KEY PERFORMANCE INDICATORS")
    
    consumo_total = df_filtro['consumo_mwh'].sum()
    custo_livre_total = df_filtro['custo_livre'].sum()
    custo_cativo_total = df_filtro['custo_cativo'].sum()
    economia_total = df_filtro['economia'].sum()
    preco_medio_ponderado = (custo_livre_total + custo_cativo_total) / consumo_total if consumo_total > 0 else 0
    economia_vs_cativo = (economia_total / custo_cativo_total * 100) if custo_cativo_total > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" data-tooltip='Consumo total no período selecionado'>
            <div class="metric-label">⚡ CONSUMO TOTAL</div>
            <div class="metric-value">{consumo_total:,.0f}</div>
            <div class="metric-delta">
                <span style='color: #2ecc71;'>●</span> {len(df_filtro['data'].unique())} meses
            </div>
            <div class="custom-progress">
                <div class="custom-progress-fill" style="width: 100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" data-tooltip='Economia vs Mercado Cativo'>
            <div class="metric-label">💰 ECONOMIA TOTAL</div>
            <div class="metric-value" style='color: #2ecc71;'>R$ {economia_total:,.0f}</div>
            <div class="metric-delta">
                <span style='color: #2ecc71;'>▼</span> {economia_vs_cativo:.1f}% vs Cativo
            </div>
            <div class="custom-progress">
                <div class="custom-progress-fill" style="width: {min(economia_vs_cativo, 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" data-tooltip='Custo total no Mercado Livre'>
            <div class="metric-label">🏭 MERCADO LIVRE</div>
            <div class="metric-value">R$ {custo_livre_total:,.0f}</div>
            <div class="metric-delta">
                <span style='color: #3498db;'>●</span> R$ {df_filtro['preco_contratado_mwh'].mean():.2f}/MWh
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" data-tooltip='Custo total no Mercado Cativo'>
            <div class="metric-label">⚙️ MERCADO CATIVO</div>
            <div class="metric-value">R$ {custo_cativo_total:,.0f}</div>
            <div class="metric-delta">
                <span style='color: #e74c3c;'>●</span> R$ {df_filtro['preco_cativo_mwh'].mean():.2f}/MWh
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card" data-tooltip='Preço médio ponderado (Livre + Cativo)'>
            <div class="metric-label">📉 PREÇO MÉDIO</div>
            <div class="metric-value">R$ {preco_medio_ponderado:,.2f}</div>
            <div class="metric-delta">
                <span style='color: #9b59b6;'>●</span> /MWh ponderado
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos da Visão Geral
    col_esq, col_dir = st.columns([1.2, 0.8])
    
    with col_esq:
        st.markdown('<div class="chart-card clickable">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 EVOLUÇÃO TEMPORAL • CUSTOS & ECONOMIA</div>', unsafe_allow_html=True)
        
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
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="Custo (R$)", gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title="Economia (R$)", overlaying="y", side="right", gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_dir:
        st.markdown('<div class="chart-card clickable">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⚡ DISTRIBUIÇÃO DE CONSUMO</div>', unsafe_allow_html=True)
        
        df_consumo_unidade = df_filtro.groupby("unidade")["consumo_mwh"].sum().reset_index()
        
        fig_rosca = go.Figure(data=[go.Pie(
            labels=df_consumo_unidade["unidade"],
            values=df_consumo_unidade["consumo_mwh"],
            hole=.65,
            marker=dict(colors=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'], line=dict(color='#1a1e24', width=2)),
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
            annotations=[dict(text=f'{consumo_total:,.0f}<br>MWh', x=0.5, y=0.5, font_size=22, font_color='white', showarrow=False)],
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_rosca, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Cards de Insight Rápidos
    st.markdown("## 🎯 INSIGHTS RÁPIDOS")
    col_insight1, col_insight2, col_insight3, col_insight4 = st.columns(4)
    
    with col_insight1:
        melhor_unidade = df_filtro.groupby('unidade')['economia'].sum().idxmax()
        melhor_economia = df_filtro.groupby('unidade')['economia'].sum().max()
        st.markdown(f"""
        <div class="insight-card" style='background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.05) 100%); border-radius: 16px; padding: 20px;'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <div style='background: rgba(46,204,113,0.2); padding: 12px; border-radius: 12px;'>🏆</div>
                <div>
                    <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>MELHOR PERFORMANCE</p>
                    <p style='color: white; margin:4px 0 0 0; font-size: 1.1rem; font-weight: 600;'>{melhor_unidade}</p>
                    <p style='color: #2ecc71; margin:0; font-size: 0.9rem;'>R$ {melhor_economia:,.0f}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight2:
        economia_media_mensal = df_filtro.groupby('data')['economia'].sum().mean()
        st.markdown(f"""
        <div class="insight-card" style='background: linear-gradient(135deg, rgba(52,152,219,0.1) 0%, rgba(52,152,219,0.05) 100%); border-radius: 16px; padding: 20px;'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <div style='background: rgba(52,152,219,0.2); padding: 12px; border-radius: 12px;'>📊</div>
                <div>
                    <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>MÉDIA MENSAL</p>
                    <p style='color: white; margin:4px 0 0 0; font-size: 1.1rem; font-weight: 600;'>R$ {economia_media_mensal:,.0f}</p>
                    <p style='color: #3498db; margin:0; font-size: 0.9rem;'>economia/mês</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight3:
        taxa_economia_media = df_filtro['economia_percentual'].mean()
        st.markdown(f"""
        <div class="insight-card" style='background: linear-gradient(135deg, rgba(241,196,15,0.1) 0%, rgba(241,196,15,0.05) 100%); border-radius: 16px; padding: 20px;'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <div style='background: rgba(241,196,15,0.2); padding: 12px; border-radius: 12px;'>📉</div>
                <div>
                    <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>TAXA DE ECONOMIA</p>
                    <p style='color: white; margin:4px 0 0 0; font-size: 1.1rem; font-weight: 600;'>{taxa_economia_media:.1f}%</p>
                    <p style='color: #f1c40f; margin:0; font-size: 0.9rem;'>vs Mercado Cativo</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_insight4:
        eficiencia_media = df_filtro['eficiencia'].mean()
        st.markdown(f"""
        <div class="insight-card" style='background: linear-gradient(135deg, rgba(155,89,182,0.1) 0%, rgba(155,89,182,0.05) 100%); border-radius: 16px; padding: 20px;'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <div style='background: rgba(155,89,182,0.2); padding: 12px; border-radius: 12px;'>⚡</div>
                <div>
                    <p style='color: #8892b0; margin:0; font-size: 0.8rem;'>EFICIÊNCIA</p>
                    <p style='color: white; margin:4px 0 0 0; font-size: 1.1rem; font-weight: 600;'>{eficiencia_media:.1f}%</p>
                    <p style='color: #9b59b6; margin:0; font-size: 0.9rem;'>preço livre/cativo</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== TAB 2: ANÁLISE FINANCEIRA =====
with tab2:
    st.markdown("## 💰 ANÁLISE FINANCEIRA DETALHADA")
    
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 COMPARATIVO DE PREÇOS • R$/MWh</div>', unsafe_allow_html=True)
        
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
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Preço (R$/MWh)"),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig_precos, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_fin2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💵 ECONOMIA ACUMULADA • POR UNIDADE</div>', unsafe_allow_html=True)
        
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
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Economia Acumulada (R$)"),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig_acumulado, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabela Financeira
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 RESUMO FINANCEIRO POR UNIDADE</div>', unsafe_allow_html=True)
    
    df_resumo_fin = df_filtro.groupby('unidade').agg({
        'consumo_mwh': 'sum',
        'custo_livre': 'sum',
        'custo_cativo': 'sum',
        'economia': 'sum',
        'economia_percentual': 'mean'
    }).round(2).reset_index()
    
    df_resumo_fin.columns = ['Unidade', 'Consumo (MWh)', 'Custo Livre (R$)', 'Custo Cativo (R$)', 
                           'Economia (R$)', 'Economia Média (%)']
    
    st.dataframe(
        df_resumo_fin,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Economia Média (%)": st.column_config.ProgressColumn(
                "Economia Média (%)",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            )
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ===== TAB 3: PERFORMANCE OPERACIONAL =====
with tab3:
    st.markdown("## ⚡ PERFORMANCE OPERACIONAL")
    
    col_op1, col_op2 = st.columns(2)
    
    with col_op1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 CONSUMO POR UNIDADE • EVOLUÇÃO</div>', unsafe_allow_html=True)
        
        fig_consumo = px.bar(
            df_filtro,
            x='data',
            y='consumo_mwh',
            color='unidade',
            barmode='group',
            color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
            labels={'data': 'Período', 'consumo_mwh': 'Consumo (MWh)', 'unidade': 'Unidade'}
        )
        
        fig_consumo.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8892b0'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig_consumo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_op2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 EFICIÊNCIA • PREÇO LIVRE VS CATIVO</div>', unsafe_allow_html=True)
        
        df_eficiencia = df_filtro.groupby('unidade')['eficiencia'].mean().reset_index()
        
        fig_eficiencia = go.Figure(go.Bar(
            x=df_eficiencia['unidade'],
            y=df_eficiencia['eficiencia'],
            marker_color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12'],
            text=df_eficiencia['eficiencia'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside',
            textfont=dict(color='white')
        ))
        
        fig_eficiencia.add_hline(y=100, line_dash="dash", line_color="#e74c3c", 
                                annotation_text="Preço Cativo", annotation_font_color="#e74c3c")
        
        fig_eficiencia.update_layout(
            height=400,
            title="Eficiência de Preço (% do Cativo)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#8892b0'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Eficiência (%)"),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        st.plotly_chart(fig_eficiencia, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Métricas Operacionais
    st.markdown("## 📊 MÉTRICAS OPERACIONAIS")
    
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    
    with col_metric1:
        consumo_medio_unidade = df_filtro.groupby('unidade')['consumo_mwh'].sum().mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 CONSUMO MÉDIO/UNIDADE</div>
            <div class="metric-value">{consumo_medio_unidade:,.0f}</div>
            <div class="metric-delta">MWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metric2:
        preco_livre_medio = df_filtro['preco_contratado_mwh'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 PREÇO MÉDIO LIVRE</div>
            <div class="metric-value">R$ {preco_livre_medio:,.2f}</div>
            <div class="metric-delta">/MWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metric3:
        preco_cativo_medio = df_filtro['preco_cativo_mwh'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚙️ PREÇO MÉDIO CATIVO</div>
            <div class="metric-value">R$ {preco_cativo_medio:,.2f}</div>
            <div class="metric-delta">/MWh</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_metric4:
        diferenca_preco = preco_cativo_medio - preco_livre_medio
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📉 DIFERENCIAL DE PREÇO</div>
            <div class="metric-value" style='color: #2ecc71;'>R$ {diferenca_preco:,.2f}</div>
            <div class="metric-delta">economia/MWh</div>
        </div>
        """, unsafe_allow_html=True)

# ===== TAB 4: PROJEÇÕES & TRENDS =====
with tab4:
    st.markdown("## 📈 PROJEÇÕES & TENDÊNCIAS")
    
    st.markdown("""
    <div style='background: rgba(46, 204, 113, 0.05); border: 1px solid rgba(46, 204, 113, 0.2); border-radius: 16px; padding: 32px; text-align: center; margin-bottom: 24px;'>
        <span style='font-size: 3rem; margin-bottom: 16px; display: block;'>🚀</span>
        <h3 style='color: white; margin-bottom: 12px;'>Módulo de Machine Learning em Desenvolvimento</h3>
        <p style='color: #8892b0; font-size: 1.1rem;'>Em breve: Previsões de consumo, detecção de anomalias e recomendações automáticas</p>
        <div style='margin-top: 24px;'>
            <span class='status-badge status-warning'>🔧 EM DESENVOLVIMENTO</span>
            <span class='status-badge status-info' style='margin-left: 12px;'>📊 PREVISÃO Q2 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Análise de Sazonalidade
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 ANÁLISE DE SAZONALIDADE</div>', unsafe_allow_html=True)
    
    df_filtro['mes_num'] = df_filtro['data'].dt.month
    df_sazonalidade = df_filtro.groupby('mes_num').agg({
        'consumo_mwh': 'mean',
        'economia': 'mean'
    }).reset_index()
    
    fig_sazonalidade = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_sazonalidade.add_trace(
        go.Bar(x=df_sazonalidade['mes_num'], y=df_sazonalidade['consumo_mwh'], 
               name="Consumo Médio", marker_color='#3498db'),
        secondary_y=False
    )
    
    fig_sazonalidade.add_trace(
        go.Scatter(x=df_sazonalidade['mes_num'], y=df_sazonalidade['economia'],
                  name="Economia Média", mode='lines+markers', line=dict(color='#2ecc71', width=3)),
        secondary_y=True
    )
    
    fig_sazonalidade.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8892b0'),
        xaxis=dict(title="Mês", tickmode='array', tickvals=list(range(1,13)), 
                   ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='white')),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    fig_sazonalidade.update_yaxes(title_text="Consumo Médio (MWh)", gridcolor='rgba(255,255,255,0.05)', secondary_y=False)
    fig_sazonalidade.update_yaxes(title_text="Economia Média (R$)", gridcolor='rgba(255,255,255,0.05)', secondary_y=True)
    
    st.plotly_chart(fig_sazonalidade, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== TAB 5: DADOS DETALHADOS (CORRIGIDO) =====
with tab5:
    st.markdown("## 🔍 DATAFRAME ANALYTICS")
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 DADOS COMPLETOS • DETALHAMENTO</div>', unsafe_allow_html=True)
    
    # Formatar dados para exibição
    df_display = df_filtro.copy()# ===== TAB 5: DADOS DETALHADOS (VERSÃO 100% CORRIGIDA) =====
with tab5:
    st.markdown("## 🔍 DATAFRAME ANALYTICS")
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 DADOS COMPLETOS • DETALHAMENTO</div>', unsafe_allow_html=True)
    
    # Formatar dados para exibição
    df_display = df_filtro.copy()
    
    # Formatar as colunas para exibição
    df_display['data'] = df_display['data'].dt.strftime('%Y-%m-%d')
    df_display['consumo_mwh'] = df_display['consumo_mwh'].apply(lambda x: f"{x:,.0f}")
    df_display['preco_contratado_mwh'] = df_display['preco_contratado_mwh'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['preco_cativo_mwh'] = df_display['preco_cativo_mwh'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['custo_livre'] = df_display['custo_livre'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['custo_cativo'] = df_display['custo_cativo'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['economia'] = df_display['economia'].apply(lambda x: f"R$ {x:,.2f}")
    
    # 🔴 CORREÇÃO DEFINITIVA: NÃO USAR df_display.columns = [...]
    # Em vez disso, criar um novo DataFrame com as colunas renomeadas
    
    # Dicionário de renomeação
    rename_dict = {
        'data': 'Data',
        'unidade': 'Unidade',
        'consumo_mwh': 'Consumo (MWh)',
        'preco_contratado_mwh': 'Preço Livre (R$/MWh)',
        'preco_cativo_mwh': 'Preço Cativo (R$/MWh)',
        'custo_livre': 'Custo Livre (R$)',
        'custo_cativo': 'Custo Cativo (R$)',
        'economia': 'Economia (R$)',
        'mes': 'Mês',
        'ano_mes': 'Ano/Mês',
        'economia_percentual': 'Economia %',
        'eficiencia': 'Eficiência %'
    }
    
    # Aplicar renomeação de forma segura
    df_display = df_display.rename(columns=rename_dict)
    
    # Selecionar apenas as colunas que queremos mostrar
    colunas_para_exibir = [
        'Data', 
        'Unidade', 
        'Consumo (MWh)', 
        'Preço Livre (R$/MWh)', 
        'Preço Cativo (R$/MWh)', 
        'Custo Livre (R$)', 
        'Custo Cativo (R$)', 
        'Economia (R$)', 
        'Economia %', 
        'Eficiência %'
    ]
    
    # Verificar se todas as colunas existem
    colunas_existentes = [col for col in colunas_para_exibir if col in df_display.columns]
    
    if len(colunas_existentes) != len(colunas_para_exibir):
        st.warning(f"⚠️ Algumas colunas não foram encontradas: {set(colunas_para_exibir) - set(colunas_existentes)}")
    
    # Filtrar apenas colunas existentes
    df_display_filtered = df_display[colunas_existentes].copy()
    
    # Filtro de pesquisa
    search_term = st.text_input("🔍 Pesquisar nos dados", placeholder="Digite unidade, período...")
    
    if search_term:
        # Aplicar filtro apenas em colunas de texto
        mask = df_display_filtered.astype(str).apply(
            lambda row: row.str.contains(search_term, case=False).any(), axis=1
        )
        df_display_filtered = df_display_filtered[mask]
    
    # Exibir dataframe
    st.dataframe(
        df_display_filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Economia %": st.column_config.ProgressColumn(
                "Economia %",
                help="Percentual de economia em relação ao mercado cativo",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "Eficiência %": st.column_config.ProgressColumn(
                "Eficiência %",
                help="Eficiência do preço contratado vs preço cativo",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            )
        }
    )
    
    # Estatísticas descritivas
    st.markdown("### 📊 ESTATÍSTICAS DESCRITIVAS")
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        st.metric("Total de Registros", len(df_filtro))
    with col_stats2:
        periodo_inicio = df_filtro['data'].min().strftime('%d/%m/%Y')
        periodo_fim = df_filtro['data'].max().strftime('%d/%m/%Y')
        st.metric("Período Analisado", f"{periodo_inicio} - {periodo_fim}")
    with col_stats3:
        st.metric("Unidades Ativas", len(df_filtro['unidade'].unique()))
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer com UX aprimorado
st.markdown("""
<div class='dashboard-footer'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div style='display: flex; gap: 24px;'>
            <span style='color: #8892b0; font-size: 0.85rem;'>⚡ DEEP DARK ANALYTICS v2.0</span>
            <span style='color: #8892b0; font-size: 0.85rem;'>•</span>
            <span style='color: #8892b0; font-size: 0.85rem;' data-tooltip='UX/UI Premium Design'>🎨 Glassmorphism UI</span>
            <span style='color: #8892b0; font-size: 0.85rem;'>•</span>
            <span style='color: #8892b0; font-size: 0.85rem;' data-tooltip='5 dashboards integrados'>📊 Multi-page Analytics</span>
        </div>
        <div style='display: flex; gap: 16px;'>
            <span class='status-badge status-success'>● SYSTEM ONLINE</span>
            <span class='status-badge status-info'>⚡ REAL-TIME</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
