FROM nvcr.io/nvidia/pytorch:23.12-py3

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    wget \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "teacher_bot.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]