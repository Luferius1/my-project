# Используем образ с веб-сервером Nginx
FROM nginx:alpine

# Копируем файлы сайта в папку /usr/share/nginx/html на контейнере
COPY . /usr/share/nginx/html
