import streamlit as st
import pandas as pd
import altair as alt

def grafico_evolucao_diversidade_paises(df):
    st.subheader("📈 Evolução da Diversidade de Países por Ano")

    # Remove nulos e cria uma linha por país por título
    df_filtrado = df[['release_year', 'country']].dropna()
    df_filtrado['country'] = df_filtrado['country'].str.split(',')
    df_explodido = df_filtrado.explode('country')
    df_explodido['country'] = df_explodido['country'].str.strip()

    # Agrupa por ano e conta quantos países distintos aparecem em cada ano
    diversidade = (
        df_explodido.groupby('release_year')['country']
        .nunique()
        .reset_index()
        .rename(columns={'country': 'Países distintos'})
    )

    chart = alt.Chart(diversidade).mark_line(point=True).encode(
        x=alt.X('release_year:O', title='Ano'),
        y=alt.Y('Países distintos:Q', title='Número de Países Representados'),
        tooltip=['release_year', 'Países distintos']
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)
