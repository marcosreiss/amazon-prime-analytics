import streamlit as st
import altair as alt

def grafico_top_generos(df):
    st.subheader("🎭 Top 10 Gêneros Mais Comuns")

    tipo = st.radio(
        "Filtrar por Tipo:",
        ["Todos", "Filmes", "Séries"],
        horizontal=True
    )

    if tipo == "Filmes":
        df = df[df['type'] == 'Movie']
    elif tipo == "Séries":
        df = df[df['type'] == 'TV Show']

    generos = (
        df['listed_in']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )
    generos.columns = ['Gênero', 'Contagem']

    chart = alt.Chart(generos).mark_bar().encode(
        x=alt.X('Contagem:Q', title='Número de Títulos'),
        y=alt.Y('Gênero:N', sort='-x', title='Gênero'),
        tooltip=['Gênero', 'Contagem']
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)
