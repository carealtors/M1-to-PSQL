FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose necessary port (if applicable)
EXPOSE 8000
