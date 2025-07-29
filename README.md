# 📊 Dashboard Amazon Prime (Topcix 2025.1)

Este projeto apresenta um dashboard interativo com Streamlit baseado em dados da Amazon Prime Video, com foco em análise exploratória e visualização de métricas relevantes.

---

## 📁 Estrutura do Projeto

```
topcix_dashboard/
├── data/
│   └── amazon_prep.csv           # Dataset tratado
├── outputs/
│   └── *.png                     # Gráficos gerados pelo script de EDA
├── scripts/
│   └── eda_report.py             # Script de análise exploratória
├── streamlit_dashboard.py        # Dashboard principal com Streamlit
├── requirements.txt              # Dependências do projeto
└── README.md                     # Instruções e descrição
```

---

## ▶️ Executando Localmente

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/topcix_dashboard.git
cd topcix_dashboard
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Execute o dashboard:

```bash
streamlit run streamlit_dashboard.py
```

---

## 📈 Scripts Disponíveis

### Análise Exploratória (offline):

```bash
python scripts/eda_report.py
```

Gera gráficos em PNG na pasta `outputs/` com base no dataset tratado.

---

## 🔍 Funcionalidades do Dashboard

* Identificação do usuário via sidebar
* Métricas principais (número de lançamentos, duração média, etc)
* Gráficos interativos com Altair:

  * Lançamentos por ano
  * Distribuição de tipos
  * Top 10 gêneros
  * Duração média dos filmes
* Layout organizado com navegação via sidebar

---

## 👨‍🏫 Atividade Topcix (2025.1)

Atende aos critérios da atividade:

1. Identificação de usuário
2. Questões de negócio
3. Métricas e indicadores
4. Gráficos
5. Layout claro
6. Demonstração funcional via Python/Streamlit

---

## 📌 Requisitos

* Python 3.8+
* Streamlit
* pandas
* altair
* matplotlib (opcional, para script EDA)
* seaborn (opcional, para script EDA)

---

## ✍️ Autor

Projeto desenvolvido para a disciplina Topcix 2025.1

---

Qualquer dúvida, abra um issue ou envie uma mensagem.
