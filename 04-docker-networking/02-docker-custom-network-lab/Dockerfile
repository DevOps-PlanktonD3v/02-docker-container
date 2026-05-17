FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    dnsutils \
    net-tools \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
