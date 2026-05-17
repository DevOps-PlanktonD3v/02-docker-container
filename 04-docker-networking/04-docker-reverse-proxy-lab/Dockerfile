FROM node:22-alpine

WORKDIR /app

RUN apk add --no-cache \
    curl \
    iputils \
    bind-tools \
    net-tools

COPY package.json .
RUN npm install --omit=dev

COPY app.js .

EXPOSE 3000

CMD ["node", "app.js"]
