# Use Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy project files
COPY . /app

# Expose port
EXPOSE 5000

# Start the backend app
CMD ["python", "-m", "backend.app"]
