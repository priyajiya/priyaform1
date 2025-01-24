# Stage 1: Build stage
FROM python:3.9-slim AS builder

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final stage
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application files
COPY . /app

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

