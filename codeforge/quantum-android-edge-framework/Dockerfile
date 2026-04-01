FROM python:3.11-slim

WORKDIR /app

# Install build dependencies and create non-root user
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        python3-dev \
        python3-pip \
        build-essential \
        libpq-dev \
        libffi-dev \
        libssl-dev && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --no-color -r requirements.txt

# Copy application code
COPY src/ src/

# Change ownership of app files to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Setup entrypoint
ENTRYPOINT ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Build stage
FROM python:3.11-slim
LABEL org.opencontainers.image.source="https://github.com/quantum-android-edge-framework"
LABEL org.opencontainers.image.description="Quantum Android Edge Framework Backend"
LABEL org.opencontainers.image.licenses="MIT"

# Copy installed packages from builder
COPY --from=0 /app /app
COPY --from=0 /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create app directory and set permissions
WORKDIR /app
RUN mkdir -p src/backend/logs && \
    chown -R 1000:1000 /app

# Set non-root user
USER 1000

# Copy application code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --no-color -r requirements.txt

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["python3", "src/backend/main.py"]