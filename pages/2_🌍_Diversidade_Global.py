import streamlit as st
import pandas as pd
import altair as alt
import pycountry_convert as pc

st.set_page_config(page_title="Diversidade Global", layout="wide")
st.title("🌍 Diversidade Global no Catálogo da Amazon Prime")

df = pd.read_csv("data/amazon_prep_with_release_year.csv")

# === Prepara coluna de países (explode multi-países) ===
paises = (
    df['country']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
)

# === Top 20 países mais presentes ===
top_paises = (
    paises.value_counts()
    .head(20)
    .reset_index()
)
top_paises.columns = ['País', 'Contagem']

with st.container():
    st.subheader("🏳️ Top 20 Países com Mais Títulos")
    chart = alt.Chart(top_paises).mark_bar().encode(
        x=alt.X('Contagem:Q', title='Número de Títulos'),
        y=alt.Y('País:N', sort='-x'),
        tooltip=['País', 'Contagem']
    ).properties(height=350)
    st.altair_chart(chart, use_container_width=True)

# === Mapeamento de países para continentes ===
def obter_continente(pais):
    try:
        codigo = pc.country_name_to_country_alpha2(pais)
        continente = pc.country_alpha2_to_continent_code(codigo)
        nomes = {
            "NA": "América do Norte",
            "SA": "América do Sul",
            "EU": "Europa",
            "AF": "África",
            "AS": "Ásia",
            "OC": "Oceania"
        }
        return nomes.get(continente, "Outro")
    except:
        return "Outro"

# === Agrupa por continente ===
df_continente = pd.DataFrame({'País': paises})
df_continente['Continente'] = df_continente['País'].apply(obter_continente)
dados_continentes = df_continente['Continente'].value_counts().reset_index()
dados_continentes.columns = ['Continente', 'Contagem']

with st.container():
    st.subheader("🗺️ Distribuição por Continente")
    chart = alt.Chart(dados_continentes).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Contagem", type="quantitative"),
        color=alt.Color(field="Continente", type="nominal"),
        tooltip=["Continente", "Contagem"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

# === Evolução temporal por país específico ===
st.subheader("📈 Evolução de Títulos ao Longo do Tempo por País")

# Prepara dados por país + ano
df_ano = df[['release_year', 'country']].dropna()
df_ano['country'] = df_ano['country'].str.split(',').explode().str.strip()
df_ano['release_year'] = pd.to_numeric(df_ano['release_year'], errors='coerce')
df_ano = df_ano[df_ano['release_year'].notna()]

paises_unicos = sorted(df_ano['country'].unique())
pais_escolhido = st.selectbox("Selecione um país para análise temporal:", paises_unicos)

dados_filtrados = (
    df_ano[df_ano['country'] == pais_escolhido]
    .groupby('release_year')
    .size()
    .reset_index(name='Quantidade')
)

linha = alt.Chart(dados_filtrados).mark_line(point=True).encode(
    x=alt.X('release_year:O', title='Ano'),
    y=alt.Y('Quantidade:Q', title='Nº de Lançamentos'),
    tooltip=['release_year', 'Quantidade']
).properties(height=350)

st.altair_chart(linha, use_container_width=True)
