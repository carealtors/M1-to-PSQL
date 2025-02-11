# Use the official Node.js image
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy app source
COPY . .

# Build the app
RUN npm run build

# Serve the app
CMD ["npm", "start"]

# Expose React dev server port
EXPOSE 3000
