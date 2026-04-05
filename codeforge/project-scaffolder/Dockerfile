FROM python:3.7-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Copy source code
COPY src/ src/
COPY setup.py .

# Install the application in development mode
RUN pip install --user -e .

FROM python:3.7-slim

# Create non-root user
RUN groupadd -r appuser \
    && useradd -r -g appuser -d /app -s /bin/bash appuser \
    && mkdir -p /app /output \
    && chown -R appuser:appuser /app /output

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY --from=builder /app /app

# Set proper permissions
RUN chown -R appuser:appuser /home/appuser/.local

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Create output directory
RUN mkdir -p /app/output

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import click, cookiecutter, yaml; print('OK')" || exit 1

# Set entrypoint for the application
ENTRYPOINT ["project-scaffolder"]
CMD ["--help"]

# Set working directory as volume for output files
VOLUME ["/output"]