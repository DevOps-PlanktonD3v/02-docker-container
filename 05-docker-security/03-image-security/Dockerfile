# ============================================================
# Stage 1 — builder
# Full Node image: install dependencies & copy source
# ============================================================
FROM node:22-alpine AS builder

WORKDIR /app

COPY package.json .
RUN npm install --omit=dev

COPY app.js .

# ============================================================
# Stage 2 — production (distroless)
# No shell, no package manager, no OS tools — minimal attack surface
# ============================================================
FROM gcr.io/distroless/nodejs22-debian12

WORKDIR /app

# Copy only what the app needs from the builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/app.js .

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Distroless has no shell — CMD must use exec form
CMD ["app.js"]
