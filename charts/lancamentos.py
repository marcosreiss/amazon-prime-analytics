import streamlit as st
import altair as alt
import pandas as pd

def grafico_lancamentos_por_ano(df):
    st.subheader("Lançamentos por Ano")

    # Define intervalo dos anos disponíveis
    min_ano = int(df['release_year'].min())
    max_ano = int(df['release_year'].max())

    # Slider com layout dedicado
    with st.container():
        st.markdown("###### Filtrar por Período")
        ano_inicio, ano_fim = st.slider(
            "Intervalo de anos",
            min_value=min_ano,
            max_value=max_ano,
            value=(min_ano, max_ano),
            step=1,
            label_visibility="collapsed"  # deixa o layout limpo
        )

    # Filtra os dados
    lanc = (
        df[df['release_year'].between(ano_inicio, ano_fim)]
        ['release_year']
        .value_counts()
        .sort_index()
        .reset_index()
    )
    lanc.columns = ['Ano', 'Quantidade']

    # Gráfico
    chart = alt.Chart(lanc).mark_bar().encode(
        x=alt.X('Ano:O', title='Ano', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Quantidade:Q', title='Número de Títulos'),
        tooltip=['Ano', 'Quantidade']
    ).properties(
        height=350,
        width='container'  # usa largura disponível do container
    )

    st.altair_chart(chart, use_container_width=True)
