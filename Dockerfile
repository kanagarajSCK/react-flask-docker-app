# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install backend dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Build React frontend
WORKDIR /app/client
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install
RUN npm run build

# Move frontend build into Flask static directory
WORKDIR /app
RUN mkdir -p server/static && cp -r client/build/* server/static/

# Expose Flask port
EXPOSE 5000

# Start Flask backend
WORKDIR /app/server
CMD ["python", "app.py"]
