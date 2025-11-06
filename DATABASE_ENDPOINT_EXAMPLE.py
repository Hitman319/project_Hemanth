"""
Simple Database Example - Add this to your hello.py file
"""

# Add these imports to hello.py
from sqlalchemy.orm import Session
from app.models.database import get_db, User
from fastapi import Depends

# Add this endpoint to your hello.py router
@router.get("/database-info")
async def get_database_info(db: Session = Depends(get_db)):
    """
    Get database information - simple database connection example
    """
    try:
        # Count users in database
        user_count = db.query(User).count()
        
        # Get all users
        users = db.query(User).all()
        
        # Prepare user list
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "name": user.name, 
                "email": user.email,
                "created_at": str(user.created_at)
            })
        
        return {
            "database_type": "SQLite",
            "database_file": "./app.db", 
            "connection_status": "Connected",
            "total_users": user_count,
            "users": user_list
        }
        
    except Exception as e:
        return {
            "database_type": "SQLite",
            "connection_status": "Error",
            "error": str(e)
        }

@router.post("/create-user")
async def create_test_user(db: Session = Depends(get_db)):
    """
    Create a test user - simple database write example
    """
    try:
        # Create a new user with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        new_user = User(
            name=f"User_{timestamp}",
            email=f"user_{timestamp}@example.com"
        )
        
        # Add to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "status": "success",
            "message": "User created successfully",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "created_at": str(new_user.created_at)
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create user: {str(e)}"
        }
