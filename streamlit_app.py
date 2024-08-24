import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Configuração inicial do dashboard com cores e identidade visual da Stone
st.set_page_config(
    page_title='Dashboard Stone',
    page_icon=':credit_card:',  # Ícone de cartão de crédito
    layout="wide",
)

# CSS customizado para aplicar as cores da Stone
st.markdown("""
    <style>
        .main { background-color: #f5f5f5; } /* Fundo claro */
        h1, h2, h3, h4 { color: #00c83b; } /* Verde Stone nos títulos */
        .stSlider { color: #00c83b; } /* Slider com verde Stone */
        .stButton>button { background-color: #00c83b; color: white; } /* Botões verdes */
        .stMultiSelect>div { background-color: #00c83b; color: white; } /* Multiselect verde */
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Função para carregar os dados

@st.cache_data
def get_data():
    """Carrega e processa os dados."""
    # Substitua o caminho do arquivo pelo dataset relevante
    DATA_FILENAME = Path(__file__).parent / 'data/stone_data.csv'
    raw_df = pd.read_csv(DATA_FILENAME)

    # Processamento de dados conforme necessário
    df = raw_df.melt(
        ['Identificador'],
        [str(x) for x in range(2010, 2024)],  # Anos de exemplo, ajustar conforme necessário
        'Ano',
        'Valor'
    )

    df['Ano'] = pd.to_numeric(df['Ano'])
    return df

df = get_data()

# -----------------------------------------------------------------------------
# Interface do usuário

# Título do dashboard com estilo da Stone
st.title(':money_with_wings: Dashboard de Desempenho Stone')

# Breve descrição do dashboard
st.markdown("""
Explore os dados de desempenho para diferentes identificadores ao longo dos anos.
Os dados são fictícios e servem para ilustrar como pode ser construído um dashboard interativo.
""")

# Filtros
min_ano = df['Ano'].min()
max_ano = df['Ano'].max()

anos_selecionados = st.slider(
    'Selecione o intervalo de anos:',
    min_value=min_ano,
    max_value=max_ano,
    value=[min_ano, max_ano]
)

identificadores = df['Identificador'].unique()

if not len(identificadores):
    st.warning("Selecione pelo menos um identificador")

identificadores_selecionados = st.multiselect(
    'Selecione os identificadores:',
    identificadores,
    identificadores[:3]  # Seleciona os três primeiros por padrão
)

# Filtragem de dados
df_filtrado = df[
    (df['Identificador'].isin(identificadores_selecionados)) &
    (df['Ano'] >= anos_selecionados[0]) &
    (df['Ano'] <= anos_selecionados[1])
]

# -----------------------------------------------------------------------------
# Visualizações

# Gráfico de linha
st.header('Desempenho ao longo do tempo')
st.line_chart(
    df_filtrado,
    x='Ano',
    y='Valor',
    color='Identificador'
)

# Métricas finais para o último ano selecionado
st.header(f'Valores no ano de {anos_selecionados[1]}')

colunas = st.columns(4)

for i, identificador in enumerate(identificadores_selecionados):
    col = colunas[i % len(colunas)]

    with col:
        primeiro_valor = df_filtrado[df_filtrado['Ano'] == anos_selecionados[0]][df_filtrado['Identificador'] == identificador]['Valor'].iat[0]
        ultimo_valor = df_filtrado[df_filtrado['Ano'] == anos_selecionados[1]][df_filtrado['Identificador'] == identificador]['Valor'].iat[0]

        if math.isnan(primeiro_valor):
            crescimento = 'n/a'
            delta_color = 'off'
        else:
            crescimento = f'{ultimo_valor / primeiro_valor:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{identificador} Valor',
            value=f'{ultimo_valor:,.0f}',
            delta=crescimento,
            delta_color=delta_color
        )
