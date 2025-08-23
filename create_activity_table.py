from app import app
from connectDB import db

with app.app_context():
    db.create_all()  # This will only create the missing 'activities' table
    print("✅ 'activities' table created.")
