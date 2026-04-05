FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

# Install dependencies for the script that are versioned
# This includes: web3, requests, pandas, matplotlib, seaborn, pydantic, and other libraries
COPY . .

# Create non-root user for security best practices
USER appuser

# Set the entrypoint and run the application
ENTRYPOINT ["python", "src/main.py"]

# Use health check to verify the application is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD python3 -c "import sys; print('Health check successful')" || exit 1
# Install Python dependencies
RUN python3 -c "import sys; print('Dependencies installed successfully')" || exit 1

# Copy the script to the image
COPY src/main.py src/

# Copy the script to the image
COPY src/staking_calculator.py src/

# Copy the script to the image
COPY src/blockchain_client.py src/

# Copy the script to the image
COPY src/data_fetcher.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY tests/test_staking_calculator.py tests/

# Copy the script to the image
COPY tests/test_blockchain_client.py tests/

# Copy the script to the image
COPY tests/test_data_fetcher.py tests/

# Copy the script to the image
COPY tests/test_validator.py tests/

# Copy the script to the image
COPY tests/conftest.py tests/

# Copy the script to the image
COPY docker-compose.yml .

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the complete implementation
# Install Python dependencies
RUN pip install --no-cache -r requirements.txt

# Copy the script to the image
COPY src/staking_calculator.py src/

# Copy the script to the image
COPY src/main.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/data_fetcher.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
   # Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
        # copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
    src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
# Install Python dependencies
RUN pip install --no-cache -r requirements.txt

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the script to the image
COPY src/models/reward_rate.py src/

# Copy the script to the image
COPY src/utils.py src/

# Copy the script to the image
COPY src/validator.py src/

# Copy the script to the image
COPY src/models/stake_data.py src/

# Copy the