
FROM node:18-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build



FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

RUN mkdir -p /usr/share/nginx/html/retail

COPY --from=build /app/dist /usr/share/nginx/html/retail

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]