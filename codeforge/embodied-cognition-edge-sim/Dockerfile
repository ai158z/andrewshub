# Multi-stage build for embodied-cognition-edge-sim
# Build stage
FROM python:3.8-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libpython3-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy python requirements
COPY setup.py setup.py
COPY src/ src/

# Install Python dependencies
RUN pip install --no-cache-dir --user -e .

# Production stage
FROM python:3.8-slim

# Install ROS 2 Foxy
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /tmp/ros.key \
    && apt-key add /tmp/ros.key \
    && sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list' \
    && apt-get update \
    && apt-get install -y ros-foxy-ros-base \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/* \
    && rosdep init || true

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy built files from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY --from=builder /app /app
WORKDIR /app

# Install application
RUN pip install --no-cache-dir --user -e .

# Set environment variables
ENV ROS_DISTRO=foxy
ENV ROS_ROOT=/opt/ros/$ROS_DISTRO
ENV ROS_PACKAGE_PATH=/opt/ros/$ROS_DISTRO/share
ENV PATH=$ROS_ROOT/bin:$PATH
ENV LD_LIBRARY_PATH=$ROS_ROOT/lib:$LD_LIBRARY_PATH
ENV CMAKE_PREFIX_PATH=$ROS_ROOT

# Create non-root user
USER appuser

# Set working directory
WORKDIR /app

# Expose ports if needed
EXPOSE 11345

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD python3 -c "import rclpy; print('Health check passed')"

# Default command
CMD ["ros2", "launch", "embodied_edge_sim", "simulation.launch.py"]