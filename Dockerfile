# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# تثبيت المتطلبات
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# نسخ كود الباكенд والواجهة
COPY backend/ /app/
COPY frontend/ /app/frontend/

# تأكد أن التطبيق يستمع على 0.0.0.0:PORT
EXPOSE 8080
CMD ["python", "-m", "app"]
