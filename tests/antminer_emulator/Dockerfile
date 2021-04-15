FROM nginx:alpine

COPY nginx.conf /etc/nginx/
COPY cgi-bin /usr/share/nginx/html/cgi-bin

# Never use password as plain text. Here we simplify process of testing.
RUN echo root:{PLAIN}root > /usr/share/nginx/.htpasswd

CMD ["nginx","-g","daemon off;"]