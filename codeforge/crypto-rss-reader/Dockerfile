# Use multi-stage build for a minimal final image
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=${DATABASE_URL} \
    REDIS_URL=${REDIS_URL} \
    MOONPAY_API_KEY=${MOONPAY_API_KEY}

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src
COPY migrations/ ./migrations

# Create non-root user
RUN addgroup --system crypto && \
    adduser --system --group crypto

# Switch to final stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=${DATABASE_URL} \
    REDIS_URL=${REDIS_URL} \
    MOONPAY_API_KEY=${MOONPAY_API_KEY}

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy python dependencies from builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Change ownership of app files to non-root user
RUN chown -R crypto:crypto /app

# Create data directory for SQLite
RUN mkdir -p /app/data && \
    chown -R crypto:crypto /app/data

# Switch to non-root user
USER crypto

# Set working directory permissions
WORKDIR /app

# Command to run the application
ENTRYPOINT ["python", "src/main.py"]

# Health check - verify the app starts without errors
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python src/main.py --health-check || exit 1

# Expose port if needed (for web interface in future)
# EXPOSE 8000

# Define volume for persistent data
VOLUME ["/app/data"]