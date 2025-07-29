import streamlit as st
import altair as alt

def grafico_duracao(df):
    st.subheader("⏱️ Duração Média de Filmes")
    filmes = df[df['type'] == 'Movie']
    media = filmes['duration_minutes'].dropna().mean()
    st.metric(label="Duração Média (min)", value=f"{media:.1f}")

    hist = alt.Chart(filmes).mark_bar().encode(
        x=alt.X('duration_minutes', bin=alt.Bin(maxbins=30), title='Duração (min)'),
        y=alt.Y('count()', title='Contagem')
    ).properties(height=300)

    st.altair_chart(hist, use_container_width=True)
