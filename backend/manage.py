#!/usr/bin/env python3
"""Management script for database operations."""
import sys
from app import create_app
from app.db import db
from app.seeds import seed_database


def main():
    """Main entry point for management commands."""
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        print("Commands: seed")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "seed":
        app = create_app()
        with app.app_context():
            seed_database()
            print("✅ Database seeded successfully!")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
