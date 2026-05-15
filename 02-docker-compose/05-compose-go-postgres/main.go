package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	_ "github.com/lib/pq"
)

type Config struct {
	Port       string
	DBHost     string
	DBPort     string
	DBUser     string
	DBPassword string
	DBName     string
}

func loadConfig() Config {
	return Config{
		Port:       getEnv("PORT", "8080"),
		DBHost:     getEnv("DB_HOST", "localhost"),
		DBPort:     getEnv("DB_PORT", "5432"),
		DBUser:     getEnv("DB_USER", "postgres"),
		DBPassword: getEnv("DB_PASSWORD", "postgres"),
		DBName:     getEnv("DB_NAME", "postgres"),
	}
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}

func writeJSON(w http.ResponseWriter, status int, data any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

func main() {
	cfg := loadConfig()

	dsn := fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		cfg.DBHost, cfg.DBPort, cfg.DBUser, cfg.DBPassword, cfg.DBName,
	)

	db, err := sql.Open("postgres", dsn)
	if err != nil {
		log.Fatalf("failed to open db: %v", err)
	}
	defer db.Close()

	mux := http.NewServeMux()

	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]any{
			"app": "go-postgres",
			"db_host": cfg.DBHost,
			"db_port": cfg.DBPort,
			"endpoints": map[string]string{
				"GET /":        "app info",
				"GET /health":  "health check",
				"GET /db-check": "test database connection",
			},
		})
	})

	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{
			"status": "ok",
		})
	})

	mux.HandleFunc("GET /db-check", func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		start := time.Now()
		var dbTime time.Time
		err := db.QueryRowContext(ctx, "SELECT NOW()").Scan(&dbTime)
		elapsed := time.Since(start)

		if err != nil {
			writeJSON(w, http.StatusServiceUnavailable, map[string]any{
				"status":  "error",
				"db_host": cfg.DBHost,
				"db_port": cfg.DBPort,
				"error":   err.Error(),
			})
			return
		}

		writeJSON(w, http.StatusOK, map[string]any{
			"status":      "connected",
			"db_host":     cfg.DBHost,
			"db_port":     cfg.DBPort,
			"db_time":     dbTime.Format(time.RFC3339),
			"latency_ms":  elapsed.Milliseconds(),
		})
	})

	addr := ":" + cfg.Port
	log.Printf("Server running on %s", addr)
	log.Printf("DB target: %s:%s/%s", cfg.DBHost, cfg.DBPort, cfg.DBName)

	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("server error: %v", err)
	}
}
