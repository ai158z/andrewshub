# Build arguments
ARG PYTHON_VERSION=3.9
ARG POETRY_VERSION=1.5.1

# Start from a Python base image
FROM python:${PYTHON_VERSION} as base

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the source code
COPY src/quantum_sensors /app/src/quantum_sensors
COPY tests /app/tests

# Install the library
RUN pip install .

# Run the application
CMD ["python", "main.py"]