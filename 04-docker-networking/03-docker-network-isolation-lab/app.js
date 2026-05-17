const express = require("express");
const { createClient } = require("redis");

const app = express();
const PORT = process.env.PORT || 3000;

const REDIS_HOST = process.env.REDIS_HOST || "localhost";
const REDIS_PORT = process.env.REDIS_PORT || 6379;

function createRedisClient() {
  return createClient({
    socket: { host: REDIS_HOST, port: Number(REDIS_PORT) },
  });
}

app.get("/", (req, res) => {
  res.json({
    app: "express-networking-lab",
    message: "Docker Network Isolation Lab - Express + Redis",
    endpoints: ["/", "/health", "/redis-check"],
  });
});

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.get("/redis-check", async (req, res) => {
  const client = createRedisClient();
  try {
    await client.connect();
    await client.set("ping", "pong");
    const value = await client.get("ping");
    res.json({
      status: "connected",
      redis_host: REDIS_HOST,
      redis_port: REDIS_PORT,
      ping: value,
    });
  } catch (err) {
    res.status(500).json({
      status: "error",
      redis_host: REDIS_HOST,
      redis_port: REDIS_PORT,
      error: err.message,
    });
  } finally {
    await client.quit().catch(() => {});
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
