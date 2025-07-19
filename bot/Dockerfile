FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        libexpat1 \
        libgeos-dev \
        libgdal-dev \
        libproj-dev \
        libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip certifi && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
