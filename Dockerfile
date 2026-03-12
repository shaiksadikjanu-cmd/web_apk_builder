# Use a Python image that also has Java installed
FROM python:3.9-slim

# Install Java (Required for apktool)
RUN apt-get update && apt-get install -y default-jdk && apt-get clean

# Set working directory
WORKDIR /app

# Copy your project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Start the server
CMD ["python", "app.py"]
