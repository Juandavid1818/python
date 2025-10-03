# --- Build del front ---
FROM node:22-alpine AS build
WORKDIR /app
COPY appweb/package*.json ./
RUN npm ci
COPY appweb/ .
RUN npm run build

# --- Servir estático con Nginx y proxy /api ---
FROM nginx:1.27-alpine
# copia el build
COPY --from=build /app/dist /usr/share/nginx/html
# nginx.conf con SPA + proxy a backend
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

# Cloud Run usa 8080
EXPOSE 8080
CMD ["nginx","-g","daemon off;"]
