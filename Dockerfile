FROM nginx:1.27-alpine
COPY index.html privacy.html styles.css favicon.svg /usr/share/nginx/html/
COPY d/ /usr/share/nginx/html/d/
EXPOSE 80
