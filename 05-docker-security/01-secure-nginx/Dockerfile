FROM nginx:alpine

# Create non-root user with explicit UID
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

    # Copy hardened nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Pre-create writable runtime dirs that nginx needs under /tmp
# (so --read-only filesystem still allows writes to /tmp only)
RUN mkdir -p /tmp/nginx \
    /tmp/nginx/proxy_temp \
    /tmp/nginx/fastcgi_temp \
    /tmp/nginx/uwsgi_temp \
    /tmp/nginx/scgi_temp \
    /tmp/nginx/client_temp && \
    chown -R appuser:appgroup /tmp/nginx

# Set minimal permissions on nginx html dir (read-only is fine)
RUN chown -R appuser:appgroup /usr/share/nginx/html && \
    chmod -R 555 /usr/share/nginx/html

# nginx config and mime types: read-only by appuser
RUN chown -R appuser:appgroup /etc/nginx && \
    chmod -R 444 /etc/nginx/nginx.conf

# Drop root — all subsequent instructions and the running container use appuser
USER appuser

# Non-privileged port (>1024 requires no CAP_NET_BIND_SERVICE)
EXPOSE 8080

# Healthcheck so you can see liveness without extra tooling
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s \
    CMD wget -qO- http://127.0.0.1:8080 || exit 1

CMD ["nginx", "-g", "daemon off;"]
