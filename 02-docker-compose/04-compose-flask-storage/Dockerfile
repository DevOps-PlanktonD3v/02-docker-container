FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=5000
ENV UPLOAD_FOLDER=/app/uploads

# folder default — bisa di-override oleh volume/bind mount
RUN mkdir -p /app/uploads

EXPOSE 5000

CMD ["python", "app.py"]
