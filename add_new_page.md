
# 🧩 Como adicionar novas páginas no dashboard prime video

Se desejar expandir o projeto com outras visualizações ou seções, basta seguir os passos abaixo:

## ✅ Etapas:

1. **Crie um novo arquivo Python na pasta `pages/`**  
   Exemplo:
   ```bash
   pages/nova_pagina.py
   ```

   Conteúdo básico:
   ```python
   import streamlit as st

   def nova_pagina(df):
       st.title("📄 Nova Página")
       st.write("Conteúdo da nova página aqui...")
   ```

2. **Adicione a nova opção de navegação no menu lateral**  
   Edite o arquivo `components/sidebar.py`:

   ```python
   def sidebar():
       st.sidebar.title("📂 Navegação")
       return st.sidebar.radio("Escolha uma tela:", [
           "🏠 Visão Geral",
           "📄 Nova Página"
       ])
   ```

3. **Importe a função da nova página no `app.py`**  
   Exemplo:
   ```python
   from pages.nova_pagina import nova_pagina
   ```

4. **Adicione a nova rota ao `app.py`**  
   No trecho de roteamento:

   ```python
   if tela == "🏠 Visão Geral":
       home(df)
   elif tela == "📄 Nova Página":
       nova_pagina(df)
   ```

---

## 📌 Resultado:

Com esses passos, o dashboard reconhecerá automaticamente a nova opção no menu lateral e exibirá a nova página sem afetar as demais.
