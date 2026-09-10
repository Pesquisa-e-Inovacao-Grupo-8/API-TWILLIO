FROM python:3.12-slim

# Evita arquivos .pyc e garante logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação
COPY . .

# Flask/Gunicorn
EXPOSE 8090

CMD ["gunicorn", "--bind", "0.0.0.0:8090", "app:app"]
