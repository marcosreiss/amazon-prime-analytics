import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Curiosidades e Destaques", layout="wide")

st.title("📌 Curiosidades e Destaques do Catálogo")

df = pd.read_csv("data/amazon_prep_with_release_year.csv")

# === Top Filmes por Duração ===
filmes = df[df['type'] == 'Movie'].copy()
filmes['duracao_min'] = pd.to_numeric(filmes['duration'].str.extract(r'(\d+)')[0], errors='coerce')
filmes_longos = (
    filmes[['title', 'duracao_min', 'release_year']]
    .dropna()
    .sort_values(by='duracao_min', ascending=False)
    .head(10)
)

with st.container():
    st.subheader("🎥 Filmes Mais Longos")
    st.dataframe(
        filmes_longos.rename(columns={
            "title": "Título", 
            "duracao_min": "Duração (min)", 
            "release_year": "Ano", 
            # "country": "País"
        }),
        use_container_width=True
    )

# === Top Séries por Temporadas ===
series = df[df['type'] == 'TV Show'].copy()
series['temporadas'] = pd.to_numeric(series['duration'].str.extract(r'(\d+)')[0], errors='coerce')
series_longas = (
    series[['title', 'temporadas', 'release_year']]
    .dropna()
    .sort_values(by='temporadas', ascending=False)
    .head(10)
)

with st.container():
    st.subheader("📺 Séries com Mais Temporadas")
    st.dataframe(
        series_longas.rename(columns={
            "title": "Título", 
            "temporadas": "Temporadas", 
            "release_year": "Ano", 
            # "country": "País"
        }),
        use_container_width=True
    )

# === Diversidade Global ===
top_paises = (
    df['country']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)
top_paises.columns = ['País', 'Contagem']

with st.container():
    st.subheader("🌍 Diversidade Global de Produção")
    chart = alt.Chart(top_paises).mark_bar().encode(
        x=alt.X('Contagem:Q', title='Número de Títulos'),
        y=alt.Y('País:N', sort='-x'),
        tooltip=['País', 'Contagem']
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)

# === Títulos com Elenco Mais Numeroso ===
df['qtd_atores'] = df['cast'].fillna('').apply(lambda x: len(x.split(',')))
mais_atores = (
    df[df['qtd_atores'] > 5]
    .sort_values(by='qtd_atores', ascending=False)
    .head(10)[['title', 'qtd_atores', 'type', 'release_year']]
)

with st.container():
    st.subheader("✨ Títulos com Elenco Mais Numeroso")
    st.dataframe(
        mais_atores.rename(columns={
            "title": "Título", 
            "qtd_atores": "Qtde de Atores", 
            "type": "Tipo", 
            "release_year": "Ano"
        }),
        use_container_width=True
    )
