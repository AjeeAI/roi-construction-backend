# Backend Dockerfile - ROi Construction AI Assistant
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies specified in your requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual backend code (main.py, etc.)
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]