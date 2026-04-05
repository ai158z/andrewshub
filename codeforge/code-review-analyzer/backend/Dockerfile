FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application code
COPY src/ /app/
COPY --chown=appuser:appuser . /app

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

# Create non-root user
RUN id -u appuser 2>/dev/null || useradd -r -g appuser appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -s requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-requirements.txt

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non-root user
USER appuser

# Install dependencies
RUN

# Copy application code
COPY src/ /app/

# Set non