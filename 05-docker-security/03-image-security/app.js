const express = require("express");

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.json({
    app: "Node.js Image Security Demo",
    node_version: process.version,
    environment: process.env.NODE_ENV || "development",
    endpoints: ["/", "/health"],
  });
});

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
