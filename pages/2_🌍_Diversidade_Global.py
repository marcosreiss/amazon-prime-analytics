import streamlit as st
import pandas as pd
import altair as alt
import pycountry_convert as pc
import pycountry
import plotly.express as px

st.set_page_config(page_title="Diversidade Global", layout="wide")
st.title("🌍 Diversidade Global no Catálogo da Amazon Prime")

# === Carregamento e pré-processamento ===
df = pd.read_csv("data/amazon_prep_with_release_year.csv")
df = df[df['country'].notna()]
df = df[~df['country'].str.contains("País de origem desconhecido", case=False, na=False)]
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

# Explode países compostos
df_exploded = df.copy()
df_exploded['country'] = df_exploded['country'].str.split(',')
df_exploded = df_exploded.explode('country')
df_exploded['country'] = df_exploded['country'].str.strip()

# === Top 20 Países ===
top_paises = (
    df_exploded['country']
    .value_counts()
    .head(20)
    .reset_index()
)
top_paises.columns = ['Pais', 'Contagem']  # Aqui garantimos os nomes certos

top_paises['Pais'] = top_paises['Pais'].astype(str)
top_paises['Contagem'] = pd.to_numeric(top_paises['Contagem'], errors='coerce')


st.subheader("🏳️ Top 20 Países com Mais Títulos")
chart = alt.Chart(top_paises).mark_bar().encode(
    x=alt.X('Contagem:Q', title='Número de Títulos'),
    y=alt.Y('Pais:N', sort='-x'),
    tooltip=['Pais', 'Contagem']
).properties(height=350)
st.altair_chart(chart, use_container_width=True)

# === Distribuição por Continente ===
def obter_continente(pais):
    try:
        codigo = pycountry.countries.lookup(pais).alpha_2
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

df_exploded['Continente'] = df_exploded['country'].apply(obter_continente)
df_continente = df_exploded['Continente'].value_counts().reset_index()
df_continente.columns = ['Continente', 'Contagem']

st.subheader("🗺️ Distribuição por Continente")
chart = alt.Chart(df_continente).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Contagem", type="quantitative"),
    color=alt.Color(field="Continente", type="nominal"),
    tooltip=["Continente", "Contagem"]
).properties(height=400)
st.altair_chart(chart, use_container_width=True)

# === Mapa Mundi ===
st.subheader("🗺️ Mapa Global de Títulos")
map_data = df_exploded['country'].value_counts().reset_index()
map_data.columns = ['country', 'count']

def country_to_iso3(pais):
    try:
        return pycountry.countries.lookup(pais).alpha_3
    except:
        return None

map_data['iso_alpha'] = map_data['country'].apply(country_to_iso3)
map_data = map_data.dropna(subset=['iso_alpha'])

fig = px.choropleth(
    map_data,
    locations="iso_alpha",
    color="count",
    hover_name="country",
    color_continuous_scale=px.colors.sequential.Viridis,
    projection="natural earth"
)

fig.update_geos(
    showcoastlines=False,
    showland=True,
    landcolor="lightgray",
    showocean=True,
    oceancolor="aliceblue",
    showframe=False,
    showcountries=True,
    countrycolor="white"
)

fig.update_layout(
    height=550,
    margin={"r":0,"t":30,"l":0,"b":0},
    title=dict(
        text="",
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    coloraxis_colorbar=dict(
        title="Quantidade",
        ticks="outside"
    )
)

st.plotly_chart(fig, use_container_width=True)


# === Evolução temporal ===
st.subheader("📈 Evolução de Títulos ao Longo do Tempo por País")
df_ano = df_exploded[['release_year', 'country']].dropna()

# Filtra apenas países com mais de X títulos (ex: 5)
paises_com_mais_de_5 = (
    df_ano['country'].value_counts()
    .loc[lambda x: x > 5]
    .index
    .sort_values()
)

pais_escolhido = st.selectbox("Selecione um país para análise temporal:", paises_com_mais_de_5)

df_filtrado = (
    df_ano[df_ano['country'] == pais_escolhido]
    .groupby('release_year')
    .size()
    .reset_index(name='Quantidade')
)

linha = alt.Chart(df_filtrado).mark_line(point=True).encode(
    x=alt.X('release_year:O', title='Ano'),
    y=alt.Y('Quantidade:Q', title='Nº de Lançamentos'),
    tooltip=['release_year', 'Quantidade']
).properties(height=350)

st.altair_chart(linha, use_container_width=True)
