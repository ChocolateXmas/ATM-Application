FROM python:3.13-slim-bullseye

# Set environment variables for clean logging and no pycache files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set working driectory
WORKDIR /app

# Install system dependencies for curses and MySQL support
RUN apt-get update && apt-get install -y \
    libncurses5-dev \
    libncursesw5-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    gcc \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

# Default command
CMD ["/bin/bash", "entrypoint.sh"]