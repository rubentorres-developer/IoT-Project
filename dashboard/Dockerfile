# Use an official Node.js runtime as a base image
FROM node:20.9.0

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/

# Install the project dependencies
RUN npm install

# Copy the entire project to the working directory
COPY . .

# Build the React app for production
RUN npm run build

# Expose the port that your app will run on
EXPOSE 3000

# Define the command to run your app
CMD ["npm", "start"]