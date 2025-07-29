import streamlit as st
import altair as alt
import pandas as pd

def grafico_duracao(df):
    st.subheader("⏱️ Duração de Títulos")

    # === Prepara dados ===
    filmes = df[df['type'] == 'Movie'].copy()
    filmes['duracao_numerica'] = pd.to_numeric(
        filmes['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    filmes = filmes[filmes['duracao_numerica'] <= 200]  # Exibe até 200 min

    series = df[df['type'] == 'TV Show'].copy()
    series['temporadas'] = pd.to_numeric(
        series['duration'].str.extract(r'(\d+)')[0], errors='coerce'
    )
    series = series[series['temporadas'] <= 13]  # Exibe até 13 temporadas

    # === Métricas ===
    col1, col2 = st.columns(2)
    col1.metric("Duração Média (Filmes)", f"{filmes['duracao_numerica'].dropna().mean():.1f} min")
    col2.metric("Média de Temporadas (Séries)", f"{series['temporadas'].dropna().mean():.1f}")

    # === Gráficos lado a lado ===
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🎬 Duração dos Filmes (até 200 min)")
        if not filmes['duracao_numerica'].dropna().empty:
            hist_filmes = alt.Chart(filmes).mark_bar().encode(
                x=alt.X('duracao_numerica:Q', bin=alt.Bin(step=20), title='Duração (min)'),
                y=alt.Y('count()', title='Contagem')
            ).properties(height=300)
            st.altair_chart(hist_filmes, use_container_width=True)

    with col4:
        st.markdown("### 📺 Temporadas das Séries (até 13)")
        if not series['temporadas'].dropna().empty:
            hist_series = alt.Chart(series).mark_bar().encode(
                x=alt.X('temporadas:Q', bin=alt.Bin(step=1), title='Número de Temporadas'),
                y=alt.Y('count()', title='Contagem')
            ).properties(height=300)
            st.altair_chart(hist_series, use_container_width=True)
