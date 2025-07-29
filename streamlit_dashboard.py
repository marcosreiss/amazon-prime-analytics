import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# === Configurações iniciais ===
st.set_page_config(page_title="Dashboard Amazon Prime", layout="wide")

# === Sidebar ===
st.sidebar.title("☰")
aba = st.sidebar.radio("", ["📊 Visão Geral"])

# === Carregamento dos dados ===
@st.cache_data
def load_data():
    df = pd.read_csv(Path("data/amazon_prep_v2.csv"))
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    if 'duration_minutes' not in df.columns and 'duration' in df.columns:
        df['duration_minutes'] = df['duration'].str.extract(r'(\\d+)').astype(float)
    return df

df = load_data()

# === Filtros ===
st.title("📺 Amazon Prime Video - Analytics")
st.markdown(
    "Explore padrões do catálogo da Amazon Prime. "
    "Visualize os tipos, gêneros, duração e evolução dos lançamentos ao longo do tempo."
)

st.markdown("### 🎛️ Filtros")
col1, col2 = st.columns(2)

with col1:
    tipo_opcao = st.selectbox("Tipo de título:", options=["Todos", "Movie", "TV Show"])
with col2:
    ano_min, ano_max = int(df['release_year'].min()), int(df['release_year'].max())
    ano_range = st.slider("Ano de lançamento:", min_value=ano_min, max_value=ano_max, value=(ano_min, ano_max))

# === Aplicação dos filtros ===
df_filtrado = df.copy()
if tipo_opcao != "Todos":
    df_filtrado = df_filtrado[df_filtrado['type'] == tipo_opcao]
df_filtrado = df_filtrado[df_filtrado['release_year'].between(ano_range[0], ano_range[1])]

# === Métricas ===
st.markdown("### 📌 Indicadores")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de títulos", len(df_filtrado))
col2.metric("Duração média (min)", f"{df_filtrado['duration_minutes'].dropna().mean():.1f}")
genero_mais_comum = df_filtrado['listed_in'].str.split(',').explode().str.strip().value_counts().idxmax()
col3.metric("Gênero mais comum", genero_mais_comum)
ano_mais_freq = df_filtrado['release_year'].mode()[0]
col4.metric("Ano mais frequente", int(ano_mais_freq))

# === Gráficos ===

# Lançamentos por ano
st.markdown("### 📈 Lançamentos por Ano")
lancamentos = df_filtrado['release_year'].value_counts().sort_index().reset_index()
lancamentos.columns = ['Ano', 'Quantidade']

chart_lanc = alt.Chart(lancamentos).mark_bar().encode(
    x=alt.X('Ano:O', title='Ano'),
    y=alt.Y('Quantidade:Q', title='Número de Títulos'),
    tooltip=['Ano', 'Quantidade']
).properties(height=300)
st.altair_chart(chart_lanc, use_container_width=True)

# Tipos
st.markdown("### 📊 Distribuição de Tipos")
tipo_counts = df_filtrado['type'].value_counts().reset_index()
tipo_counts.columns = ['Tipo', 'Quantidade']

chart_tipo = alt.Chart(tipo_counts).mark_bar().encode(
    y=alt.Y('Tipo:N', title='Tipo', sort='-x'),
    x=alt.X('Quantidade:Q', title='Quantidade'),
    color=alt.value("#5B8FA7")
).properties(height=200)
st.altair_chart(chart_tipo, use_container_width=True)

# Gêneros
st.markdown("### 🎭 Top 10 Gêneros")
generos = df_filtrado['listed_in'].str.split(',').explode().str.strip().value_counts().head(10).reset_index()
generos.columns = ['Gênero', 'Contagem']

chart_gen = alt.Chart(generos).mark_bar().encode(
    y=alt.Y('Gênero:N', title='Gênero', sort='-x'),
    x=alt.X('Contagem:Q', title='Quantidade'),
    color=alt.value("#87A922")
).properties(height=300)
st.altair_chart(chart_gen, use_container_width=True)

# Duração
st.markdown("### ⏱️ Distribuição da Duração dos Filmes")
duracoes = df_filtrado[df_filtrado['type'] == 'Movie']['duration_minutes'].dropna()

chart_dur = alt.Chart(duracoes.to_frame()).mark_bar().encode(
    x=alt.X("duration_minutes", bin=alt.Bin(maxbins=30), title="Duração (min)"),
    y=alt.Y("count()", title="Contagem"),
    tooltip=["count()"]
).properties(height=300)
st.altair_chart(chart_dur, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("📘 Dados analisados a partir do catálogo da Amazon Prime. Dashboard desenvolvido para fins educacionais na disciplina Tópicos Especiais (IFMA 2025.1).")
