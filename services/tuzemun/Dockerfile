FROM node:18-alpine

RUN mkdir /app

COPY app/package.json app/yarn.lock /app/

WORKDIR /app

RUN yarn install --frozen-lockfile

COPY app /app

RUN chmod +x start.sh

EXPOSE 8080

ENTRYPOINT /bin/sh /app/start.sh
