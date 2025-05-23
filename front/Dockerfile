# Base image
FROM python:3.12.1-slim

# Set working directory
WORKDIR /app

# Copy files
COPY front.py .

# Install dependencies
RUN pip install requests

# Run the CLI script
CMD ["python", "front.py"]
