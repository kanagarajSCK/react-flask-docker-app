# ------------ FRONTEND (React) BUILD STAGE ------------
FROM node:18 as frontend

WORKDIR /app
COPY client ./client
WORKDIR /app/client

RUN npm install
RUN npm run build


# ------------ BACKEND (Flask + OpenCV) FINAL STAGE ------------
FROM python:3.10-slim

WORKDIR /app

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

# Install Python dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend Flask code
COPY server ./server

# Copy built React frontend into Flask static folder
COPY --from=frontend /app/client/build ./server/static

WORKDIR /app/server

EXPOSE 5000

CMD ["python", "app.py"]




















# # Stage 1: Build React frontend
# FROM node:18 AS frontend

# # Set working directory
# WORKDIR /app

# # Copy frontend source code
# COPY client ./client

# # Change working directory to client and install dependencies
# WORKDIR /app/client
# RUN npm install

# # Build the React app
# RUN npm run build

# # Stage 2: Set up Flask backend with OpenCV support
# FROM python:3.10-slim AS backend

# # Set working directory
# WORKDIR /app

# # ✅ Install OpenCV system dependencies
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy Python requirements and install them
# COPY server/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy backend code
# COPY server ./server

# # ✅ Copy React build output to Flask static folder
# COPY --from=frontend /app/client/build/ ./server/static/

# # Set working directory to Flask app folder
# WORKDIR /app/server

# # Expose Flask app port
# EXPOSE 5000

# # Run the Flask app
# CMD ["python", "app.py"]
