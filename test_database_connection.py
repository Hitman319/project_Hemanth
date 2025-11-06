"""
Database Connection Test Script
"""
import asyncio
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, create_tables, User
from app.core.config import settings

def test_database_connection():
    """Test the database connection and basic operations"""
    
    print("🗄️ Testing Database Connection...")
    print(f"Database URL: {settings.database_url}")
    
    try:
        # Create tables if they don't exist
        print("📋 Creating database tables...")
        create_tables()
        print("✅ Tables created successfully!")
        
        # Test database connection
        print("🔗 Testing database connection...")
        db: Session = SessionLocal()
        
        # Test query - count users
        user_count = db.query(User).count()
        print(f"📊 Current users in database: {user_count}")
        
        # Create a test user
        print("👤 Creating test user...")
        test_user = User(
            name="Test User",
            email="test@example.com"
        )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("ℹ️ Test user already exists")
        else:
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ Created test user with ID: {test_user.id}")
        
        # Query all users
        all_users = db.query(User).all()
        print(f"👥 Total users after test: {len(all_users)}")
        
        for user in all_users:
            print(f"   - ID: {user.id}, Name: {user.name}, Email: {user.email}")
        
        db.close()
        print("✅ Database connection test successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n🎉 Database is ready for use!")
    else:
        print("\n💥 Database setup needs attention!")
