# Используем базовый образ Python
FROM python:3.9

# Создаем директорию приложения
WORKDIR /app

# Копируем файлы requirements.txt и исходный код приложения в контейнер
COPY requirements.txt requirements.txt
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Экспонируем порт 5000 (если ваше приложение слушает этот порт)
EXPOSE 5000

# Запускаем приложение с Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
