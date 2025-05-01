FROM python:3.9-slim

# Install required libraries for MariaDB and compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy files
COPY src/backend /app/backend
COPY requirements.txt .
COPY healthcheck.sh .
COPY src/backend/entrypoint.py /app/entrypoint.py

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY start.sh .

# Give execution permission to the script
RUN chmod +x start.sh

# Avvia il backend con uvicorn
CMD ["./start.sh"]
