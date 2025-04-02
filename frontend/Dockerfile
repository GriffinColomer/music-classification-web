# Use a lightweight Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Install dependencies separately for caching
COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Expose the default React port
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]