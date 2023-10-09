FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx
COPY ./conf.d/site.conf /etc/nginx/conf.d
