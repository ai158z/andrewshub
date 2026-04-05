FROM python:3.11-slim

# Create non-root user
RUN addgroup --group appgroup --gid 1001 && \
    adduser --disabled-password --uid 1001 --group appgroup --home /app

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        && \
    pip install --no-cache-dir -r requirements.txt && \
    # Cleanup to reduce image size
    apt-get purge -y --auto-remove \
        gcc \
        g++ \
        && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Change ownership of app files to non-root user
RUN chown -R 1001:1001 /app

# Switch to non-root user
USER 1001

# Expose port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run the application
CMD ["python", "src/main.py"]