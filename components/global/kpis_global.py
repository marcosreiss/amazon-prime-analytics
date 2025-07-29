import streamlit as st

def mostrar_kpis_globais(df):
    col1, col2, col3 = st.columns(3)

    # Total de países únicos com títulos
    total_paises = df['country'].dropna().str.split(',').explode().str.strip().nunique()

    # Top 1 país mais presente
    pais_mais_presente = (
        df['country']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .value_counts()
        .idxmax()
    )

    # Tipos distintos de produções (Movie, TV Show, etc.)
    tipos_distintos = df['type'].nunique()

    col1.metric("🌍 Países com Títulos", total_paises)
    col2.metric("🏆 País Mais Presente", pais_mais_presente)
    col3.metric("🎬 Tipos de Títulos", tipos_distintos)
