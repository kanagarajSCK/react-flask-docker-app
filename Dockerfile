# Step 1: Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Build React frontend
WORKDIR /app/client
RUN npm install
RUN npm run build

# Move frontend build into Flask's static directory
WORKDIR /app
RUN mkdir -p server/build && cp -r client/build/* server/build/

# Expose Flask port
EXPOSE 5000

# Run Flask app
WORKDIR /app/server
CMD ["python", "app.py"]
