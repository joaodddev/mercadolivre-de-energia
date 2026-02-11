
# Análise de Economia no Mercado Livre de Energia

## Descrição
Este projeto visa analisar a economia gerada pela migração para o mercado livre de energia para diferentes unidades consumidoras. Ele utiliza dados simulados de consumo e preços para calcular custos no mercado livre e cativo, identificando a economia potencial. Um dashboard interativo construído com Streamlit permite visualizar esses insights de forma clara e acessível.

## Funcionalidades
O dashboard Streamlit oferece as seguintes funcionalidades:
- **Exibição de KPIs**: Mostra o consumo total (MWh), custo total no mercado livre (R$), custo total no mercado cativo (R$), economia total (R$), preço médio ponderado (R$/MWh) e economia acumulada (R$).
- **Filtros Interativos**: Permite filtrar os dados por período (data) e por unidade consumidora.
- **Gráficos de Evolução Mensal**: Visualiza a evolução mensal dos custos (mercado livre e cativo) e a economia acumulada.
- **Gráficos de Consumo por Unidade**: Exibe o consumo total por cada unidade selecionada.
- **Tabela de Dados Detalhados**: Apresenta os dados brutos e os cálculos detalhados em formato de tabela.

## Como Executar

### Pré-requisitos
Para executar este projeto, você precisará ter o Python instalado (versão 3.8 ou superior).

### Instalação
1. Clone este repositório para sua máquina local:
   ```bash
   git clone <URL_DO_SEU_REPOSITÓRIO>
   cd <nome_do_seu_repositório>
   ```
2. Instale as dependências necessárias usando pip:
   ```bash
   pip install streamlit pandas
   ```

### Rodando o Dashboard
Após a instalação, você pode iniciar o dashboard Streamlit:
1. Certifique-se de que o arquivo `energia.csv` e `app.py` estejam no mesmo diretório.
2. Execute o seguinte comando no terminal:
   ```bash
   streamlit run app.py
   ```
3. O Streamlit abrirá automaticamente uma nova aba no seu navegador com o dashboard.

## Estrutura do Projeto
- `app.py`: Contém o código Python para o dashboard interativo Streamlit.
- `energia.csv`: Arquivo CSV com os dados simulados de consumo e preços de energia.
- `mercado_livre_energia.ipynb`: Notebook Jupyter/Colab que documenta o processo de desenvolvimento, cálculos e a criação do dashboard.
- `README.md`: Este arquivo, fornecendo informações sobre o projeto.
