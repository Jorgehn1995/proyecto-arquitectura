# syntax=docker/dockerfile:1.6
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
# Use BuildKit cache for pip to avoid re-downloading unchanged dependencies
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Copy application code
COPY . .

# Make wait-for-db script executable
RUN chmod +x docker/wait-for-db.sh

# Expose port
EXPOSE 8000

# Run the application
CMD ["./docker/wait-for-db.sh", "db", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:create_app()"]
