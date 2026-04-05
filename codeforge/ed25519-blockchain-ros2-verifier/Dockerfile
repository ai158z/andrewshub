FROM python:3.8-slim

WORKDIR /app

# Copy files
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Install Python dependencies
RUN pip install .

# Expose necessary ports
# (ROS2 typically uses ports 7400-7500, but can be any available port)
EXPOSE 7400

# Set working directory to the specific path for the library code
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    ros2 \
    && rm -rf /var/lib/apt/lists/*

# Install the library and clean up
RUN pip3 install \
    ed25519-blockchain-ros2-verifier

# Run tests
CMD ["python", "test_core.py"]