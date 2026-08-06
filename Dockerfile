# Base image Python 3.10 slim
FROM python:3.10-slim

# Set environment variable agar output Python langsung tampil di log
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=80

# Set direktori kerja di dalam container
WORKDIR /app

# Install dependensi sistem dasar
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements terlebih dahulu untuk caching layer Docker
COPY requirements.txt .

# Install dependensi Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi
COPY . .

# Pastikan folder upload ada
RUN mkdir -p static/uploads

# Expose port 80 di dalam container
EXPOSE 80

# Jalankan server Gunicorn binding ke 0.0.0.0:80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app"]
