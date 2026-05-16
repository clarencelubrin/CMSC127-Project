#!/bin/bash
# Fix potential Windows line endings in .env and this script
sed -i 's/\r$//' .env init.sh

# Exit immediately if any command fails
set -e

# 1. Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found in the current directory."
    exit 1
fi

# Load variables and automatically export them
set -a
source .env
set +a

echo "Starting database setup for: $MARIADB_DATABASE..."

# 2. Combine the database and user creation into a single MySQL session using a Here-Doc
mysql -u root -p"$MARIADB_ROOT_PASSWORD" <<EOF
DROP DATABASE IF EXISTS $MARIADB_DATABASE;
CREATE DATABASE $MARIADB_DATABASE;
CREATE USER IF NOT EXISTS '$MARIADB_USER'@'localhost' IDENTIFIED BY '$MARIADB_USER_PASSWORD';
GRANT ALL PRIVILEGES ON $MARIADB_DATABASE.* TO '$MARIADB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Database '$MARIADB_DATABASE' and user '$MARIADB_USER' created successfully."

# 3. Apply Schema (with file check)
if [ -f "./database/schema.sql" ]; then
    mysql -u root -p"$MARIADB_ROOT_PASSWORD" "$MARIADB_DATABASE" < ./database/schema.sql
    echo "Database schema created."
else
    echo "Error: ./database/schema.sql not found."
    exit 1
fi

# 4. Apply Seed Data (with file check)
if [ -f "./database/seed.sql" ]; then
    mysql -u root -p"$MARIADB_ROOT_PASSWORD" "$MARIADB_DATABASE" < ./database/seed.sql
    echo "Database seeded with initial data."
else
    echo "Warning: ./database/seed.sql not found. Skipping seed."
fi

echo "✅ Setup complete!"