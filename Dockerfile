# syntax=docker/dockerfile:1

# Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY data/ ./data/

# Handle BuildKit secrets and copy to application secrets directory
RUN --mount=type=secret,id=db_password \
    --mount=type=secret,id=db_user \
    --mount=type=secret,id=db_host \
    --mount=type=secret,id=db_port \
    --mount=type=secret,id=db_name \
    --mount=type=secret,id=base_url \
    --mount=type=secret,id=redis_url \
    mkdir -p /app/secrets && \
    if [ -f /run/secrets/db_password ]; then cp /run/secrets/db_password /app/secrets/db_password; fi && \
    if [ -f /run/secrets/db_user ]; then cp /run/secrets/db_user /app/secrets/db_user; fi && \
    if [ -f /run/secrets/db_host ]; then cp /run/secrets/db_host /app/secrets/db_host; fi && \
    if [ -f /run/secrets/db_port ]; then cp /run/secrets/db_port /app/secrets/db_port; fi && \
    if [ -f /run/secrets/db_name ]; then cp /run/secrets/db_name /app/secrets/db_name; fi && \
    if [ -f /run/secrets/base_url ]; then cp /run/secrets/base_url /app/secrets/base_url; fi && \
    if [ -f /run/secrets/redis_url ]; then cp /run/secrets/redis_url /app/secrets/redis_url; fi

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/v1/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]