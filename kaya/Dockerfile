# Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy Django app code
COPY . .

# Create a wait-for-it script to ensure DB is ready
# COPY ./wait-for-it.sh /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh

# CMD ["gunicorn", "kaya.wsgi:application", "--bind", "0.0.0.0:8000"]
