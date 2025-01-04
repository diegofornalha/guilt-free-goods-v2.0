FROM node:18-slim as base

# Add Python for AI/ML tasks
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Install Python dependencies
RUN pip3 install torch torchvision tensorflow transformers pillow numpy pandas

# Build the application
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]