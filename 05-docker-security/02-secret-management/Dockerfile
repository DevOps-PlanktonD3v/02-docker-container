FROM python:3.13-slim

WORKDIR /app

# Install dependencies as a separate layer for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Run as non-root user
RUN useradd --no-create-home --shell /bin/false appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
