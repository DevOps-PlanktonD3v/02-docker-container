FROM golang:1.22-alpine AS builder

WORKDIR /app

# copy semua source
COPY . .

# download dependency
RUN go mod tidy

# build binary
RUN go build -o server .

# ---- runtime image ----
FROM alpine:3.20

WORKDIR /app

COPY --from=builder /app/server .

ENV PORT=8080
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=postgres

EXPOSE 8080

CMD ["./server"]