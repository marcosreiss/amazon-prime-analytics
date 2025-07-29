import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Carregamento dos dados
df = pd.read_csv("data/amazon_prep.csv")
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Exibe informações básicas
print("\n--- Informações Gerais ---")
print(df.info())
print("\n--- Estatísticas Descritivas ---")
print(df.describe(include='all'))
print("\n--- Valores Nulos por Coluna ---")
print(df.isna().sum())

# Análise: Lançamentos por ano
releases = df['release_year'].value_counts().sort_index()
plt.figure()
releases.plot(kind='bar', title='Lançamentos por Ano')
plt.xlabel("Ano")
plt.ylabel("Número de Títulos")
plt.tight_layout()
plt.savefig("outputs/lancamentos_por_ano.png")

# Análise: Distribuição de tipos
plt.figure()
df['type'].value_counts().plot.pie(autopct='%1.1f%%', title='Distribuição de Tipos')
plt.ylabel("")
plt.tight_layout()
plt.savefig("outputs/distribuicao_tipos.png")

# Análise: Top 10 gêneros
top_genres = df['listed_in'].str.split(',').explode().str.strip().value_counts().head(10)
plt.figure()
top_genres.plot(kind='barh', title='Top 10 Gêneros')
plt.xlabel("Contagem")
plt.tight_layout()
plt.savefig("outputs/top_generos.png")

# Análise: Duração média dos filmes
movie_durations = df[df['type'] == 'Movie']['duration_minutes'].dropna()
mean_duration = movie_durations.mean()
print(f"\nDuração média dos filmes: {mean_duration:.1f} minutos")

plt.figure()
movie_durations.hist(bins=30)
plt.title("Distribuição da Duração dos Filmes")
plt.xlabel("Minutos")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig("outputs/dist_duracao.png")
