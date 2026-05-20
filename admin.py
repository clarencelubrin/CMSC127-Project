
from database.connection import DBConnection
import os
import argparse
from contextlib import contextmanager

import bcrypt
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_db():
    db = DBConnection()
    db.connect(
        user=os.getenv("MARIADB_USER"),
        password=os.getenv("MARIADB_USER_PASSWORD"),
        host=os.getenv("MARIADB_HOST", "localhost"),
        port=int(os.getenv("MARIADB_PORT", "3306")),
        database=os.getenv("MARIADB_DATABASE")
    )
    curr = db.cursor
    try:
        yield curr
        db.commit()
    finally:
        curr.close()
        db.disconnect()

def get_password_hash(password: str) -> str:
    # Hash the password and decode back to string for database storage
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_user(username: str, password: str, db):
    try:
        password_hash = get_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        return {"message": "User created successfully"}
    except Exception as e:
        return {"error": str(e)}

def delete_user(username: str, db):
    try:
        db.execute("DELETE FROM users WHERE username = %s", (username,))
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

def main():
    # Args [--create/-c | --delete/-d | --list/-l] [--username USERNAME --password PASSWORD]

    parser = argparse.ArgumentParser(description="User management for the application")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", "-c", action="store_true", help="Create a new user")
    group.add_argument("--delete", "-d", action="store_true", help="Delete an existing user")
    group.add_argument("--list", "-l", action="store_true", help="List all users")
    parser.add_argument("--username", "-u", help="Username for the user")
    parser.add_argument("--password", "-p", help="Password for the user")

    args = parser.parse_args()

    with get_db() as db:
        if args.delete:
            result = delete_user(args.username, db)
            if "error" in result:
                print(f"Error deleting user: {result['error']}")
            else:
                print(result["message"])
        elif args.create:
            result = create_user(args.username, args.password, db)
            if "error" in result:
                print(f"Error creating user: {result['error']}")
            else:
                print(result["message"])
        elif args.list:
            # Print current users
            with get_db() as db:
                db.execute("SELECT username FROM users")
                users = db.fetchall()
                print("Current users:")
                for user in users:
                    print(f"- {user[0]}")

if __name__ == "__main__":
    main()