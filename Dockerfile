# Используем образ с веб-сервером Nginx
FROM nginx:alpine

# Копируем наш конфигурационный файл в папку conf.d
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем файлы сайта в папку /usr/share/nginx/html на контейнере
COPY . /usr/share/nginx/html
