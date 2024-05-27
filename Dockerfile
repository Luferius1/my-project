# Используем образ с веб-сервером Nginx
FROM nginx:alpine

# Копируем файлы сайта из директории static в /var/www/html на контейнере
COPY static/ /var/www/html

# Определяем рабочую директорию
WORKDIR /var/www/html
