import streamlit as st
import pandas as pd

def mostrar_metricas(df):
    total_titulos = len(df)

    # Filmes
    filmes = df[df['type'] == 'Movie'].copy()
    filmes['duracao_numerica'] = pd.to_numeric(
        filmes['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    duracao_media_filmes = filmes['duracao_numerica'].dropna().mean()

    # Séries
    series = df[df['type'] == 'TV Show'].copy()
    series['temporadas'] = pd.to_numeric(
        series['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    media_temporadas = series['temporadas'].dropna().mean()

    # Gênero mais comum
    genero_mais_comum = (
        df['listed_in']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .value_counts()
        .idxmax()
    )

    # Ano mais frequente
    ano_mais_freq = df['release_year'].mode()[0]

    # Layout responsivo com columns
    cols = st.columns([1, 1, 1, 1])  # 4 colunas iguais

    cols[0].metric("Total de Títulos", total_titulos)
    cols[1].metric("Duração Média (Filmes)", f"{duracao_media_filmes:.1f} min")
    cols[2].metric("Média de Temporadas (Séries)", f"{media_temporadas:.1f}")
    cols[3].metric("Ano Mais Frequente", int(ano_mais_freq))
