FROM ubuntu:24.04

# Timezone ma'lumotlarini o'rnatish
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# System dependencies o'rnatish
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Ishchi direktoriyani yaratish
WORKDIR /app

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Python dependencies o'rnatish
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Project fayllarini ko'chirish
COPY . .

# Default port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1