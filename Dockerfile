# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

# Step 5: Copy the application code to the container
COPY . /app/

# Step 6: Expose the port the app runs on (if using Django default port)
EXPOSE 8000

