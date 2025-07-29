import streamlit as st
import altair as alt
import pandas as pd

def grafico_duracao(df):
    st.subheader("⏱️ Duração de Títulos")

    filmes = df[df['type'] == 'Movie'].copy()
    filmes['duracao_numerica'] = pd.to_numeric(
        filmes['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    filmes = filmes[filmes['duracao_numerica'] <= 200]

    series = df[df['type'] == 'TV Show'].copy()
    series['temporadas'] = pd.to_numeric(
        series['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    series = series[series['temporadas'] <= 13]

    tipo = st.radio(
        "",  # label vazio para manter layout limpo
        ["Filmes", "Séries"],
        horizontal=True
    )

    if tipo == "Filmes":
        st.markdown("### 🎬 Duração dos Filmes")
        if not filmes['duracao_numerica'].dropna().empty:
            hist = alt.Chart(filmes).mark_bar().encode(
                x=alt.X('duracao_numerica:Q', bin=alt.Bin(step=20), title='Duração (min)'),
                y=alt.Y('count()', title='Contagem')
            ).properties(height=300)
            st.altair_chart(hist, use_container_width=True)

    elif tipo == "Séries":
        st.markdown("### 📺 Temporadas das Séries")
        if not series['temporadas'].dropna().empty:
            hist = alt.Chart(series).mark_bar().encode(
                x=alt.X('temporadas:Q', bin=alt.Bin(step=1), title='Número de Temporadas'),
                y=alt.Y('count()', title='Contagem')
            ).properties(height=300)
            st.altair_chart(hist, use_container_width=True)
