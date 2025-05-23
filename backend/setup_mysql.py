#!/usr/bin/env python
import os
import sys
import MySQLdb
import getpass

def setup_mysql_database():
    """
    Set up the MySQL database for the application.
    """
    print("Setting up MySQL database for Fintech Platform...")
    
    # Get database credentials
    db_host = input("Database host [localhost]: ") or "localhost"
    db_port = input("Database port [3306]: ") or "3306"
    db_user = input("Database user [root]: ") or "root"
    db_password = getpass.getpass("Database password: ")
    db_name = input("Database name [fintech_platform]: ") or "fintech_platform"
    
    try:
        # Connect to MySQL server
        connection = MySQLdb.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            passwd=db_password
        )
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{db_name}' created or already exists.")
        
        # Grant privileges to the user
        cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        print(f"Privileges granted to user '{db_user}'.")
        
        # Create .env file with database settings
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        with open(env_file, 'w') as f:
            f.write(f"DB_NAME={db_name}\n")
            f.write(f"DB_USER={db_user}\n")
            f.write(f"DB_PASSWORD={db_password}\n")
            f.write(f"DB_HOST={db_host}\n")
            f.write(f"DB_PORT={db_port}\n")
        
        print(f"Environment variables saved to {env_file}")
        
        # Close connection
        cursor.close()
        connection.close()
        
        print("MySQL database setup completed successfully.")
        print("You can now run migrations with: python manage.py migrate")
        
    except MySQLdb.Error as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_mysql_database()