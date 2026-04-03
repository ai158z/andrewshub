# Multi-stage Dockerfile for wallet-backup-rotation service

# Build stage
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME=/app

# Set working directory
WORKDIR $APP_HOME

# Copy dependencies from builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Set PATH for python packages
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY src/ ./src/
COPY setup.py .

# Create backups directory
RUN mkdir -p /app/backups

# Change ownership to non-root user
RUN chown -R appuser:appuser $APP_HOME

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; import importlib.util; spec = importlib.util.find_spec('src.wallet_backup'); sys.exit(0 if spec is not None else 1)"

# Expose port for health check endpoint
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["python", "-m", "src.wallet_backup.cli"]

# Define volume for persistent data
VOLUME ["/app/backups"]

# Copy the application
COPY . .

# Install the package
RUN pip install --no-cache-dir --user -e .

# Command to run the application
CMD ["python", "src/wallet_backup/cli.py"]