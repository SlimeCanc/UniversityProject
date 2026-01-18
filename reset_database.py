import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.movie import db


def reset_database():
    print("🔄 Starting database reset...")

    db_files = ['movies.db', 'instance/movies.db']
    removed_count = 0

    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"🗑️ Removed: {db_file}")
            removed_count += 1

    if removed_count == 0:
        print("ℹ️ No database files found")

    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ New database created")

    print("🎉 Database reset completed!")


if __name__ == '__main__':
    reset_database()