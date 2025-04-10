# Use a lightweight Python base image
FROM python:3.8-slim

# Install SQLite dependencies
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install  -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the app's port
EXPOSE 5002

# Set the entry point to run the app
CMD ["python", "app.py"]
