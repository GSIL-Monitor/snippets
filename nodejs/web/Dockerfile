FROM node:lts-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN npm install

FROM node:lts-alpine
EXPOSE 3000
WORKDIR /app
CMD node app.js

COPY --from=0 /app /app
