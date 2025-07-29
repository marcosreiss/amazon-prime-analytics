import streamlit as st
import pandas as pd
import altair as alt

def grafico_ranking_paises(df):
    st.subheader("🌐 Top 10 Países com Mais Títulos")

    # Explode os países e conta a frequência
    paises = (
        df['country']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )
    paises.columns = ['País', 'Quantidade']

    # Gráfico horizontal
    chart = alt.Chart(paises).mark_bar().encode(
        x=alt.X('Quantidade:Q', title='Número de Títulos'),
        y=alt.Y('País:N', sort='-x', title='País'),
        tooltip=['País', 'Quantidade']
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)
