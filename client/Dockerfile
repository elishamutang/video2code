# Builder stage
FROM node:22.14.0-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Nginx stage
FROM nginx:latest

RUN apt-get update -qq && apt-get -y install certbot python3-certbot-nginx
RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]