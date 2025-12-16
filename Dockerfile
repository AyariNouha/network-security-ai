FROM python:3.10-slim

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    tcpdump \
    tshark \
    nmap \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier projet
COPY . .

EXPOSE 8000

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]