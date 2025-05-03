FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY webserver.py .
COPY templates templates/
COPY static static/

# Default config.json will be mounted as volume
RUN echo '{}' > config.json

# Expose port for web UI
EXPOSE 5000

# Run the Flask application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "webserver:app"]