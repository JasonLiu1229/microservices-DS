# Use a base image with Node.js installed
FROM node:21.7.1-bookworm

ARG MS_BASE_DIR=/ms

WORKDIR ${MS_BASE_DIR}/frontend

# Copy the frontend source code to the working directory
COPY . .

# Command to run the Vite development server
RUN npm install && npm run build
