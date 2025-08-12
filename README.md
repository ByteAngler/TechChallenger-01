# 📚 Book API – Tech Challenge Fase 1

API REST construída com **FastAPI** para consulta de livros, obtidos via *web scraping* no site [Books to Scrape](https://books.toscrape.com).  
O projeto implementa endpoints para listagem de livros, busca por título e categoria, listagem de categorias, verificação de saúde da API e atualização dos dados via scraping.

---

## 🏗 Arquitetura do Projeto

- **FastAPI** – Framework backend para APIs rápidas e tipadas.  
- **BeautifulSoup4** – Biblioteca de *web scraping* para extração de dados HTML.  
- **Pandas** – Manipulação e leitura de dados tabulares (CSV).  
- **Pydantic** – Validação e tipagem dos dados de entrada/saída.  
- **Docker** – Containerização da aplicação para fácil deploy.  
- **Railway** – Plataforma de deploy utilizada.

📂 Estrutura de pastas:
```
app/
 ├── api/
 │   └── v1/
 │       ├── books.py        # Endpoints de livros
 │       ├── categories.py   # Endpoints de categorias
 │       ├── health.py       # Endpoint de status/healthcheck
 ├── core/
 │   └── config.py           # Configurações da aplicação
 ├── models/
 │   └── book.py             # Modelo Pydantic Book
 ├── services/
 │   ├── scraper.py          # Lógica de scraping
 ├── utils/
 │   └── scraper_utilitys.py # Funções auxiliares para scraping
 ├── main.py                 # Ponto de entrada da aplicação
data/
 └── books.csv               # Base de dados local
requirements.txt
Dockerfile
```

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seuusuario/book-api.git
cd book-api
```

### 2️⃣ Configurar variáveis de ambiente
Crie um arquivo `.env` (opcional, se quiser sobrescrever configs):
```env
CSV_PATH=./data/books.csv
BASE_URL=https://books.toscrape.com
```

### 3️⃣ Rodar localmente (sem Docker)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🐳 Executando com Docker

### Build da imagem
```bash
docker build -t book-api .
```

### Rodando o container
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data book-api
```

Isso garante que o `books.csv` seja persistido localmente.

---

## 📖 Documentação das Rotas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Redireciona para o healthcheck |
| `GET` | `/api/v1/health` | Retorna status da API e integridade do CSV |
| `GET` | `/api/v1/books` | Lista todos os livros |
| `GET` | `/api/v1/books/search?title=...&category=...` | Busca por título e/ou categoria |
| `GET` | `/api/v1/categories` | Lista categorias disponíveis |
| `POST` | `/api/v1/scraping/trigger` | Executa o scraping e atualiza o CSV |

---

## 🔍 Exemplos de Chamadas

### 1. Listar todos os livros
```bash
curl http://localhost:8000/api/v1/books
```
**Resposta**:
```json
{
  "titles": [
  "A Light in the Attic",
  "Tipping the Velvet",
  "Soumission",
  "Sharp Objects",
  "Sapiens: A Brief History of Humankind",
  "The Requiem Red"
  ]
}
```

### 2. Buscar por título ou categoria
```bash
curl "http://localhost:8000/api/v1/books/search?title=A Light in the Attic"
```
**Resposta**:
```json
[
  {
    "id": 0,
    "title": "A Light in the Attic",
    "price": 51.77,
    "availability": "In stock",
    "rating": 3,
    "category": "Poetry",
    "image_url": "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
  }
]
```

### 3. Healthcheck
```bash
curl http://localhost:8000/api/v1/health
```
**Resposta**:
```json
{
  "api_status": "Online!",
  "csv_exists": true,
  "data_loaded": true,
  "has_required_columns": true
}
```

### 4. Rodar scraping manualmente
```bash
curl -X POST http://localhost:8000/api/v1/scraping/trigger
```

---

## ▶️ Execução no Railway

1. **Subir o projeto no GitHub**  
2. **Criar projeto no Railway** selecionando o repositório  
3. Railway detecta o `Dockerfile` e realiza o build  
4. Adicionar variável:
   ```
   CSV_PATH=/app/data/books.csv
   ```
5. (Opcional) Criar **Volume** no Railway e montar em `/app/data` para persistência do CSV  
6. Testar a API acessando `https://<seu-projeto>.up.railway.app/docs`

---

## 📌 Observações
- O CSV é a fonte principal de dados; rodar o scraper sobrescreve/adiciona dados.
- Proteja a rota de scraping em produção para evitar abusos.
- O deploy no Railway é feito diretamente com o Dockerfile (não há uso de docker-compose).
