# Используем образ с веб-сервером Nginx
FROM nginx:alpine

# Удаляем стандартный конфигурационный файл Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем файлы сайта из директории static в /var/www/html на контейнере
COPY static/ /var/www/html

# Копируем index.html в директорию /var/www/html на контейнере
COPY index.html /var/www/html

# Вставляем кастомную конфигурацию Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Определяем рабочую директорию
WORKDIR /var/www/html
