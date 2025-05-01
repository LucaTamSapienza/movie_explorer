FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/frontend /app
COPY templates /app/templates
COPY static /app/static

CMD ["uvicorn", "frontend:app", "--host", "0.0.0.0", "--port", "8001"]