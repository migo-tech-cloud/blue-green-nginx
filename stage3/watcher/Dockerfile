# Base Image
FROM python:3.11-slim

# Working Directory
WORKDIR /app

# Copy script
COPY watcher.py .

# Install dependencies
RUN pip install requests

# Environment variables (optional defaults)
ENV LOG_PATH=/var/log/nginx/access.log
ENV ERROR_RATE_THRESHOLD=2
ENV WINDOW_SIZE=200
ENV ALERT_COOLDOWN_SEC=300

# Command to run watcher
CMD ["python", "watcher.py"]
