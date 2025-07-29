import streamlit as st
import altair as alt
import pandas as pd

def grafico_duracao(df):
    st.subheader("⏱️ Duração de Títulos")

    col1, col2 = st.columns(2)

    # 🎬 Filmes
    filmes = df[df['type'] == 'Movie'].copy()
    filmes['duracao_numerica'] = pd.to_numeric(
        filmes['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    media_filmes = filmes['duracao_numerica'].dropna().mean()
    col1.metric("Duração Média (Filmes)", f"{media_filmes:.1f} min")

    # 📺 Séries
    series = df[df['type'] == 'TV Show'].copy()
    series['temporadas'] = pd.to_numeric(
        series['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    media_series = series['temporadas'].dropna().mean()
    col2.metric("Média de Temporadas (Séries)", f"{media_series:.1f}")

    # 📊 Histograma: Filmes
    if not filmes['duracao_numerica'].dropna().empty:
        st.markdown("### 🎬 Distribuição da Duração dos Filmes")
        hist_filmes = alt.Chart(filmes).mark_bar().encode(
            x=alt.X('duracao_numerica', bin=alt.Bin(maxbins=30), title='Duração (min)'),
            y=alt.Y('count()', title='Contagem')
        ).properties(height=300)
        st.altair_chart(hist_filmes, use_container_width=True)

    # 📊 Histograma: Séries
    if not series['temporadas'].dropna().empty:
        st.markdown("### 📺 Distribuição de Temporadas das Séries")
        hist_series = alt.Chart(series).mark_bar().encode(
            x=alt.X('temporadas', bin=alt.Bin(maxbins=15), title='Número de Temporadas'),
            y=alt.Y('count()', title='Contagem')
        ).properties(height=300)
        st.altair_chart(hist_series, use_container_width=True)
