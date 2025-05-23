#!/bin/bash

# Script to update the VPS with the latest code from the repository

# VPS connection details
VPS_HOST="144.172.103.207"
VPS_USER="manustest"
VPS_PASS="Khdsd545\$13234fg"
VPS_APP_DIR="/var/www/fintech-platform"

# Local repository details
LOCAL_REPO_DIR="$(pwd)"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting VPS update process...${NC}"

# Check if sshpass is installed
if ! command -v sshpass &> /dev/null; then
    echo -e "${YELLOW}Installing sshpass...${NC}"
    sudo apt-get update && sudo apt-get install -y sshpass
fi

# Function to execute commands on the VPS
execute_ssh_command() {
    sshpass -p "$VPS_PASS" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "$1"
}

# Function to copy files to the VPS
copy_to_vps() {
    sshpass -p "$VPS_PASS" scp -o StrictHostKeyChecking=no -r "$1" "$VPS_USER@$VPS_HOST:$2"
}

# Check if we can connect to the VPS
echo -e "${YELLOW}Testing connection to VPS...${NC}"
if execute_ssh_command "echo 'Connection successful'"; then
    echo -e "${GREEN}Connection to VPS successful.${NC}"
else
    echo -e "${RED}Failed to connect to VPS. Please check your credentials and try again.${NC}"
    exit 1
fi

# Check if the application directory exists on the VPS
echo -e "${YELLOW}Checking if application directory exists on VPS...${NC}"
if execute_ssh_command "[ -d $VPS_APP_DIR ] && echo 'Directory exists'"; then
    echo -e "${GREEN}Application directory exists on VPS.${NC}"
else
    echo -e "${RED}Application directory does not exist on VPS. Creating it...${NC}"
    execute_ssh_command "mkdir -p $VPS_APP_DIR"
fi

# Backup the current application on the VPS
echo -e "${YELLOW}Creating backup of current application on VPS...${NC}"
BACKUP_DIR="$VPS_APP_DIR-backup-$(date +%Y%m%d%H%M%S)"
execute_ssh_command "cp -r $VPS_APP_DIR $BACKUP_DIR"
echo -e "${GREEN}Backup created at $BACKUP_DIR${NC}"

# Copy the updated code to the VPS
echo -e "${YELLOW}Copying updated code to VPS...${NC}"
copy_to_vps "$LOCAL_REPO_DIR/backend" "$VPS_APP_DIR/"
copy_to_vps "$LOCAL_REPO_DIR/frontend" "$VPS_APP_DIR/"
echo -e "${GREEN}Code copied to VPS.${NC}"

# Check MySQL installation
echo -e "${YELLOW}Checking MySQL installation on VPS...${NC}"
if execute_ssh_command "command -v mysql &> /dev/null"; then
    echo -e "${GREEN}MySQL is already installed.${NC}"
else
    echo -e "${YELLOW}Installing MySQL on VPS...${NC}"
    execute_ssh_command "sudo apt-get update && sudo apt-get install -y mysql-server"
    echo -e "${GREEN}MySQL installed.${NC}"
fi

# Create MySQL database and user if they don't exist
echo -e "${YELLOW}Setting up MySQL database on VPS...${NC}"
DB_SETUP=$(cat <<EOF
CREATE DATABASE IF NOT EXISTS fintech_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'fintech_user'@'localhost' IDENTIFIED BY 'fintech_password';
GRANT ALL PRIVILEGES ON fintech_platform.* TO 'fintech_user'@'localhost';
FLUSH PRIVILEGES;
EOF
)

execute_ssh_command "echo \"$DB_SETUP\" | sudo mysql"
echo -e "${GREEN}MySQL database setup completed.${NC}"

# Create .env file for database configuration
echo -e "${YELLOW}Creating .env file for database configuration...${NC}"
ENV_CONTENT=$(cat <<EOF
DB_NAME=fintech_platform
DB_USER=fintech_user
DB_PASSWORD=fintech_password
DB_HOST=localhost
DB_PORT=3306
NOWPAYMENTS_API_KEY=K-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX
NOWPAYMENTS_API_SECRET=S-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX
NOWPAYMENTS_IPN_SECRET=IPN-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX
NOWPAYMENTS_PRODUCTION=false
SITE_URL=https://pyscalp.com
EOF
)

execute_ssh_command "echo \"$ENV_CONTENT\" > $VPS_APP_DIR/backend/.env"
echo -e "${GREEN}.env file created successfully.${NC}"

# Install dependencies on the VPS
echo -e "${YELLOW}Installing backend dependencies on VPS...${NC}"
execute_ssh_command "cd $VPS_APP_DIR/backend && pip install -r requirements.txt"
echo -e "${GREEN}Backend dependencies installed.${NC}"

echo -e "${YELLOW}Installing frontend dependencies on VPS...${NC}"
execute_ssh_command "cd $VPS_APP_DIR/frontend && npm install"
echo -e "${GREEN}Frontend dependencies installed.${NC}"

# Run database migrations
echo -e "${YELLOW}Running database migrations on VPS...${NC}"
execute_ssh_command "cd $VPS_APP_DIR/backend && python manage.py migrate"
echo -e "${GREEN}Database migrations completed.${NC}"

# Build the frontend
echo -e "${YELLOW}Building frontend on VPS...${NC}"
execute_ssh_command "cd $VPS_APP_DIR/frontend && npm run build"
echo -e "${GREEN}Frontend built successfully.${NC}"

# Restart the application services
echo -e "${YELLOW}Restarting application services on VPS...${NC}"
execute_ssh_command "sudo systemctl restart gunicorn"
execute_ssh_command "sudo systemctl restart nginx"
echo -e "${GREEN}Application services restarted.${NC}"

echo -e "${GREEN}VPS update completed successfully!${NC}"
echo -e "${YELLOW}You can access the application at http://$VPS_HOST${NC}"

exit 0