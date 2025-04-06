# Use official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=production
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libportaudio2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs screenshots

# Expose the application port
EXPOSE 8000

# Set the entrypoint
ENTRYPOINT ["python", "neurofusion_ai.py"]