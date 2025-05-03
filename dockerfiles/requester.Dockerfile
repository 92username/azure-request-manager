FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY requester.py .

# Default config.json will be mounted as volume
RUN echo '{}' > config.json

# Create logs directory
RUN mkdir -p logs

# Expose port for Prometheus metrics
EXPOSE 8001

# Run the request script
CMD ["python", "requester.py"]