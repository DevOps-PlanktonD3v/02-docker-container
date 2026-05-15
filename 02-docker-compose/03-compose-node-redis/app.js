const express = require("express");
const redis = require("redis");

const PORT = process.env.PORT || 3000;
const REDIS_HOST = process.env.REDIS_HOST || "localhost";
const REDIS_PORT = process.env.REDIS_PORT || 6379;

const app = express();

const client = redis.createClient({
  socket: { host: REDIS_HOST, port: Number(REDIS_PORT) },
});

client.on("error", (err) => console.error("Redis error:", err));

async function connect() {
  await client.connect();
  console.log(`Connected to Redis at ${REDIS_HOST}:${REDIS_PORT}`);
}

app.get("/", async (req, res) => {
  const visitors = await client.incr("visitors");
  res.json({ message: "Hello from Node!", visitors });
});

app.get("/health", (req, res) => {
  res.json({ status: "ok", redis: client.isReady ? "connected" : "disconnected" });
});

connect().then(() => {
  app.listen(PORT, () => console.log(`App running on port ${PORT}`));
});
