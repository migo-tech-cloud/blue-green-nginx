FROM python:3.11-slim

WORKDIR /app

# Copy the watcher script
COPY watcher.py .

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "watcher.py"]

