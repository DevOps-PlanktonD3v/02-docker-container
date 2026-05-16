FROM node:22-alpine

WORKDIR /app

COPY package.json .
RUN npm install --omit=dev

COPY app.js .

ENV PORT=3000

EXPOSE 3000

CMD ["node", "app.js"]
