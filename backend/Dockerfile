# Используйте базовый образ Python
FROM python:3.11-slim

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию
WORKDIR /djangoTestStripe

# Установите зависимости Python
COPY ./requirements.txt /djangoTestStripe/
COPY ./main.py /djangoTestStripe/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Скопируйте все файлы проекта в рабочую директорию
COPY ./djangoTestStripe/ ./
