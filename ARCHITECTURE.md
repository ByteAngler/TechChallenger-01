# Plano Arquitetural

## 1. Pipeline de Dados

O fluxo de dados da aplicação segue as seguintes etapas:

1. **Ingestão**
   - Coleta de dados por meio de Web Scraping utilizando `BeautifulSoup`.
   - Fonte utilizada: [Books to Scrape](https://books.toscrape.com/).
   - Detecção e prevenção de duplicatas para manter a integridade dos dados.

2. **Processamento**
   - Limpeza e padronização das informações.
   - Estruturação em formato tabular (DataFrame do Pandas).
   - Armazenamento em arquivo CSV (`data/books.csv`).

3. **API**
   - Exposição dos dados via **FastAPI**.
   - Rotas implementadas:
     - `/api/v1/books` – Lista de livros.
     - `/api/v1/categories` – Lista de categorias.
     - `/api/v1/health` – Verificação de saúde da API e disponibilidade do CSV.
     - `/api/v1/scraping` – Atualiza os dados manualmente via scraping.

4. **Consumo**
   - Qualquer cliente HTTP pode consumir os dados (ex.: aplicações web, scripts Python, notebooks Jupyter, etc.).
   - Documentação interativa via **Swagger UI** (`/docs`).

---

## 2. Arquitetura para Escalabilidade Futura

A arquitetura foi planejada para permitir expansão futura:

- **Camadas bem definidas**: `services`, `models`, `api` e `utils`.
- Separação de responsabilidades para facilitar manutenção.
- Possibilidade de troca da camada de persistência (CSV → Banco de Dados relacional ou NoSQL).
- Uso de **Docker** para garantir reprodutibilidade e facilidade no deploy.

---

## 3. Cenário de Uso para Cientistas de Dados / ML

- Os dados extraídos e disponibilizados via API podem ser consumidos por cientistas de dados diretamente em notebooks.
- Cenários possíveis:
  - Treinamento de modelos de recomendação de livros.
  - Análise de padrões de preços por categoria.
  - Previsão de avaliações com base em histórico.

---

## 4. Plano de Integração com Modelos de ML

- Adição de um módulo `ml` na pasta `app` para hospedar scripts de pré-processamento e inferência.
- Rotas adicionais na API para:
  - `/api/v1/recommendations` – Recomendação personalizada.
  - `/api/v1/predictions` – Previsão de métricas com base em dados históricos.
- Pipeline de atualização contínua:
  - Scraping regular (job agendado ou webhook).
  - Treinamento/re-treinamento automático do modelo.
  - Deploy do modelo em container separado ou como parte do mesmo serviço.

---

## 5. Diagrama de Alto Nível

```
+------------------+       +------------------+       +-------------------+
|   Web Scraping   | --->  |   Processamento  | --->  |       CSV         |
| (BeautifulSoup)  |       |   (Pandas)       |       |   (data/books)    |
+------------------+       +------------------+       +-------------------+
                                                              |
                                                              v
                                                       +--------------+
                                                       |   FastAPI    |
                                                       |   Endpoints  |
                                                       +--------------+
                                                              |
                                                              v
                                                     +------------------+
                                                     |   Consumidores   |
                                                     | (Web, Scripts,   |
                                                     |  ML Models, etc.)|
                                                     +------------------+
```
