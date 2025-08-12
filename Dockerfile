# ===== Base =====
FROM python:3.12-slim

# Evita bytecode e força flush do stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Pasta de trabalho
WORKDIR /app

# Instala dependências do sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o código
COPY app /app/app
# Copia a pasta de dados (opcional — você pode montar volume depois)
COPY data /app/data

# Variável lida pelo Settings (pydantic-settings)
ENV CSV_PATH=/app/data/books.csv

# Porta da API
EXPOSE 8000

# Healthcheck simples
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD \
  curl -fsS http://127.0.0.1:8000/api/v1/health || exit 1

# Comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
