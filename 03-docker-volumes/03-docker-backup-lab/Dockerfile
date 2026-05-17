FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py ./

# Buat folder shared sebagai default
# (akan di-override oleh Docker Volume saat runtime)
RUN mkdir -p /shared/uploads

EXPOSE 5000

CMD ["python", "app.py"]
