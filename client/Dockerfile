# client/Dockerfile

# Step 1: Build the React app
FROM node:20 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Optional: Custom Nginx config
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
