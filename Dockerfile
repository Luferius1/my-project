# Используем базовый образ Python
FROM python:3.9

# Создаем директорию приложения
WORKDIR /app

# Копируем исходный код приложения в контейнер
COPY . .

# Создаем и активируем виртуальное окружение
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Устанавливаем зависимости
RUN . /venv/bin/activate && pip install --upgrade pip && pip install flask datetime sqlalchemy psycopg2

# Экспонируем порт 5000 (если ваше приложение слушает этот порт)
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
