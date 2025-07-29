import streamlit as st
import altair as alt

def grafico_top_generos(df):
    st.subheader("🎭 Top 10 Gêneros Mais Comuns")
    generos = df['listed_in'].str.split(',').explode().str.strip().value_counts().head(10).reset_index()
    generos.columns = ['Gênero', 'Contagem']

    chart = alt.Chart(generos).mark_bar().encode(
        x=alt.X('Gênero:O', sort='-y'),
        y=alt.Y('Contagem:Q'),
        tooltip=['Gênero', 'Contagem']
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)
