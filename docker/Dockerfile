FROM nginx:1.15-alpine
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir -p /diablo
COPY diablo/dist /diablo/dist
COPY nginx-site.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD nginx
