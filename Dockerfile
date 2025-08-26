FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 FLASK_CONFIG=development PORT=8080
WORKDIR /app

# 必要パッケージ（あなたの内容でOK）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libpq-dev pkg-config sqlite3 libsqlite3-dev libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.3.1+cpu torchvision==0.18.1+cpu

COPY . .
EXPOSE 8080
# ★ ここが肝心：: $PORT で待受 & wsgi:app を指定
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "wsgi:app"]
