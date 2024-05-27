# Используем образ с веб-сервером Nginx
FROM nginx:alpine

# Удаляем стандартный конфигурационный файл Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем файлы сайта в папку /usr/share/nginx/html на контейнере
COPY . /usr/share/nginx/html

# Вставляем нашу кастомную конфигурацию прямо внутрь стандартного конфигурационного файла
RUN echo "server {" > /etc/nginx/conf.d/default.conf
RUN echo "    listen 80;" >> /etc/nginx/conf.d/default.conf
RUN echo "    server_name localhost;" >> /etc/nginx/conf.d/default.conf
RUN echo "    root /usr/share/nginx/html;" >> /etc/nginx/conf.d/default.conf
RUN echo "    index index.html;" >> /etc/nginx/conf.d/default.conf
RUN echo "}" >> /etc/nginx/conf.d/default.conf
