import streamlit as st
from utils.load_data import load_data
from components.metrics import mostrar_metricas
from charts.lancamentos import grafico_lancamentos_por_ano
from charts.tipos import grafico_tipos
from charts.generos import grafico_top_generos
from charts.duracao import grafico_duracao

st.set_page_config(
    page_title="Dashboard Amazon Prime",
    layout="wide",
    page_icon="📺"
)

df = load_data()

def home(df):
    st.set_page_config(page_title="Visão Geral", layout="wide")
    st.title("📊 Visão Geral do Catálogo Amazon Prime")
    st.markdown("Explore os principais indicadores do catálogo da Amazon Prime Video.")

    mostrar_metricas(df)
    col1, col2 = st.columns(2)
    with col1:
        grafico_lancamentos_por_ano(df)
    with col2:
        grafico_duracao(df)
        
    col1, col2 = st.columns(2)

    with col1:
        grafico_top_generos(df)
    with col2:
        grafico_tipos(df)

    
    
home(df)

st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.8rem;'>"
    "Feito com ❤️ para a disciplina de Tópicos Especiais - IFMA 2025"
    "</div>",
    unsafe_allow_html=True
)
