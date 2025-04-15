#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Wait for MySQL Server to be ready
echo "[-] Waiting for MySQL to be ready..."

# Read the MySQL password from secrets file
DB_PASSWORD=$(cat /run/secrets/db_user_password)

# Set a timeout counter
max_attempts=30
counter=0

# Check MySQL connection with proper credentials
until mysqladmin ping -h "$DB_HOST" -u atm_user -p "$DB_PASSWORD" --silent; do 
    counter=$((counter + 1))
    if [ $counter -gt $max_attempts ]; then
        echo "[!] ERROR: Could not connect to MySQL after $max_attempts attempts. Exiting..."
        exit 1
    fi
    echo "[-] Still waiting for MySQL... (attempt $counter/$max_attempts)"
    sleep 2
done

# initialize the database
echo "[✓] MySQL is up, initializing the database..."
python init_db.py

# Start the application
echo "[✓] Starting the application..."
exec python main.py