import streamlit as st
import altair as alt

def grafico_tipos(df):
    st.subheader("Distribuição por Tipo")
    tipo = df['type'].value_counts().reset_index()
    tipo.columns = ['Tipo', 'Contagem']

    chart = alt.Chart(tipo).mark_arc().encode(
        theta=alt.Theta(field='Contagem', type='quantitative'),
        color=alt.Color(field='Tipo', type='nominal'),
        tooltip=['Tipo', 'Contagem']
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)
