# Use the official Python 3.11 slim base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (needed by some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (Cloud Run provides PORT dynamically)
EXPOSE 8080

# Default environment variables for Streamlit
ENV PORT=8080 \
    STREAMLIT_SERVER_PORT=$PORT \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false

# Run Streamlit (shell form ensures $PORT is expanded dynamically)
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
