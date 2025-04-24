#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Read the MySQL password from secrets file
MYSQL_ROOT_PASSWORD=$(cat /run/secrets/mysql_root_password)
DB_HOST=${DB_HOST:-"db"}
DB_USER=$(cat /run/secrets/mysql_user) 

# Wait for MySQL Server to be ready
echo "[-] Waiting for MySQL to be ready..."

# Set a timeout counter
max_attempts=30
counter=0

# Check MySQL connection with proper credentials
until mysqladmin ping -h "$DB_HOST" -u "$DB_USER" -p"$MYSQL_ROOT_PASSWORD" ; do 
    counter=$((counter + 1))
    if [ $counter -gt $max_attempts ]; then
        echo "entrypoint.sh | [!] ERROR: Could not connect to MySQL after $max_attempts attempts. Exiting..."
        exit 1
    fi
    echo "entrypoint.sh | [-] Still waiting for MySQL... (attempt $counter/$max_attempts)"
    sleep 2
done

# initialize the database
echo "entrypoint.sh | [✓] MySQL is up, initializing the database..."
python init_db.py
echo "entrypoint.sh | [✓] Database initialized."

# Start the application
echo "entrypoint.sh | [✓] Starting the application..."
exec python main.py || { echo "Failed to start main.py"; exit 1; }