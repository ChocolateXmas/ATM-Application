### Stage 1: Build dependencies and install packages
FROM python:3.13-slim-bullseye AS builder

# Set Working Directory
WORKDIR /app

# Install system dependencies for curses and MySQL support
RUN apt-get update && apt-get install -y \
    libncurses5-dev \
    libncursesw5-dev \
    gcc \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

RUN chmod +x entrypoint.sh

### Stage 2: Clean Runtime Image
FROM python:3.13-slim-bullseye

# Set environment variables for clean logging and no pycache files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    # default-libmysqlclient-dev \
    default-mysql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY --from=builder /app .

# Default command
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
