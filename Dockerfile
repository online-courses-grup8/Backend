FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=edutics.settings

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN --mount=type=secret,id=SECRET_KEY \
    SECRET_KEY=$(cat /run/secrets/SECRET_KEY) python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "edutics.wsgi:application", "--bind", "0.0.0.0:8000"]