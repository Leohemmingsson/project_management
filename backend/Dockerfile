FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose a port if your app serves via HTTP (optional, e.g., 8000)
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
