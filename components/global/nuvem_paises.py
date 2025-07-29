import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def nuvem_de_paises(df):
    st.subheader("🌍 Nuvem de Palavras dos Países Mais Presentes")

    # Prepara os dados
    paises = df['country'].dropna().str.split(',')
    todos_paises = paises.explode().str.strip()
    frequencias = todos_paises.value_counts().to_dict()

    # Gera a nuvem de palavras
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(frequencias)

    # Exibe o gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
