# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy watcher script and requirements
COPY watcher.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (runtime will override via .env)
ENV PYTHONUNBUFFERED=1

# Start watcher
CMD ["python", "watcher.py"]
