# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm -v && node -v

# Install Python dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Build React frontend
WORKDIR /app/client
RUN npm install && npm run build

# ✅ Check that build succeeded (for debugging)
RUN ls -la build

# Move frontend build into Flask's static directory
WORKDIR /app
RUN mkdir -p server/build && cp -r client/build/* server/build/

# Expose Flask port
EXPOSE 5000

# Run Flask app
WORKDIR /app/server
CMD ["python", "app.py"]
