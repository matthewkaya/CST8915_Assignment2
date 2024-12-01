# partners/Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5003

# Command to run the application
CMD ["python", "partners.py"]