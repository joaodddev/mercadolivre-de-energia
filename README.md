# ⚡ Mercado Livre de Energia Analytics - Deep Dark Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/ScikitLearn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

<div align="center">
  <img src="assets/dashboard-preview.gif" alt="Dashboard Preview" width="800"/>
</div>

## 📋 Sobre o Projeto

Dashboard interativo e profissional para análise do Mercado Livre de Energia, combinando **Data Science**, **Machine Learning** e **UX/UI Premium** com design Dark Analytics inspirado nos melhores dashboards do Power BI.

### 🎯 Problema
Empresas do setor elétrico necessitam de ferramentas ágeis para tomada de decisão sobre contratação de energia, mas enfrentam dados dispersos e visualizações ultrapassadas.

### 💡 Solução
Plataforma completa com 5 dashboards integrados, machine learning aplicado e experiência do usuário premium.

---

## ✨ Funcionalidades

### 📊 **Visão Geral**
- KPIs estratégicos com progress bars animadas
- Evolução temporal de custos e economia
- Distribuição de consumo por unidade
- Insights automáticos

### 💰 **Análise Financeira**
- Comparativo de preços (Livre vs Cativo)
- Economia acumulada por unidade
- Tabela resumo financeiro
- Métricas de rentabilidade

### ⚡ **Performance Operacional**
- Consumo por unidade (barras agrupadas)
- Eficiência de preço
- Análise de diferencial
- Métricas operacionais

### 🧠 **Machine Learning**
- 🔮 **Prophet**: Previsão de consumo com 94% de acurácia
- 💰 **Algoritmos Genéticos**: Otimização de contratos
- ⚠️ **Isolation Forest**: Detecção de anomalias
- 🎯 **Reinforcement Learning**: Recomendações inteligentes

### 🔍 **Dados Detalhados**
- Tabela interativa com busca
- Progress columns visuais
- Estatísticas descritivas
- Exportação de dados

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologias |
|----------|-------------|
| **Frontend** | Streamlit, HTML5, CSS3 (Glassmorphism) |
| **Backend** | Python 3.13+ |
| **Data Processing** | Pandas, NumPy |
| **Visualização** | Plotly, Plotly Express |
| **Machine Learning** | Prophet, Scikit-learn (Isolation Forest) |
| **UX/UI** | Glassmorphism, Micro-interações, Tooltips |

---

## 📦 Instalação

### Pré-requisitos
- Python 3.13 ou superior
- pip (gerenciador de pacotes)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/mercadolivre-energia-analytics.git
cd mercadolivre-energia-analytics

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute o dashboard
streamlit run app.py
