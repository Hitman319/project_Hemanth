# 📊 **Database Connection Guide for Your FastAPI Project**

## 🗄️ **Current Database Setup**

### **Database Type: SQLite**
Your FastAPI application is configured to use **SQLite**, which is:
- ✅ **File-based database** stored as `app.db`
- ✅ **Zero configuration** - no server setup required
- ✅ **Perfect for development** and small to medium applications
- ✅ **SQL compliant** - supports standard SQL operations

### **Database Connection Details**

**Current Configuration:**
```python
# .env file
DATABASE_URL=sqlite:///./app.db

# config.py
database_url: str = "sqlite:///./app.db"
```

**What this means:**
- **Protocol**: `sqlite://` - SQLite database
- **Path**: `./app.db` - Database file in project root
- **Auto-creation**: File is created automatically when first accessed

## 🔧 **How Database Connection Works**

### **1. Database Engine Setup (app/models/database.py)**
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()
```

### **2. Database Models**
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### **3. Database Session Management**
```python
def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 🚀 **How to Use Database in FastAPI Endpoints**

### **Basic CRUD Operations**

#### **1. Create (POST)**
```python
@router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
```

#### **2. Read (GET)**
```python
@router.get("/users/", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

#### **3. Update (PUT)**
```python
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.name = user_update.name
    user.email = user_update.email
    db.commit()
    db.refresh(user)
    
    return user
```

#### **4. Delete (DELETE)**
```python
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user_id} deleted successfully"}
```

## 📋 **Database Schema Management**

### **Current Schema (User Table)**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR,
    email VARCHAR UNIQUE,
    created_at DATETIME
);
```

### **View Database Schema**
You can examine your database using:

**1. SQLite Browser (GUI):**
- Download: https://sqlitebrowser.org/
- Open file: `app.db` in your project directory

**2. Command Line:**
```bash
# Windows
sqlite3 app.db
.schema users
.exit
```

**3. Python Script:**
```python
import sqlite3
conn = sqlite3.connect('app.db')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()
```

## 🧪 **Testing Database Connection**

### **Manual Test Script** (`test_database_connection.py`)
```python
from app.models.database import SessionLocal, create_tables, User

def test_database():
    # Create tables
    create_tables()
    
    # Test connection
    db = SessionLocal()
    user_count = db.query(User).count()
    print(f"Total users: {user_count}")
    
    # Create test user
    test_user = User(name="Test User", email="test@example.com")
    db.add(test_user)
    db.commit()
    
    db.close()
    print("Database test successful!")

if __name__ == "__main__":
    test_database()
```

**Run the test:**
```bash
python test_database_connection.py
```

## 🔄 **Database Migration to Other Databases**

### **PostgreSQL** (Production Ready)
```python
# .env
DATABASE_URL=postgresql://username:password@localhost/dbname

# requirements.txt
psycopg2-binary==2.9.7
```

### **MySQL**
```python
# .env  
DATABASE_URL=mysql+pymysql://username:password@localhost/dbname

# requirements.txt
pymysql==1.1.0
```

### **No Code Changes Needed!**
SQLAlchemy automatically handles different database types.

## 📊 **Current Database Status**

✅ **Database File**: `app.db` (created automatically)  
✅ **Connection**: Working (`test_database_connection.py` passed)  
✅ **Tables**: `users` table created  
✅ **Test Data**: 1 test user exists  
✅ **ORM**: SQLAlchemy configured and working  

## 🛠️ **Common Database Operations**

### **1. Add New Model**
```python
# app/models/database.py
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### **2. Create Tables**
```python
# Run once to create new tables
from app.models.database import Base, engine
Base.metadata.create_all(bind=engine)
```

### **3. Database Queries**
```python
# Basic queries
users = db.query(User).all()                    # Get all
user = db.query(User).filter(User.id == 1).first()  # Get by ID
users = db.query(User).filter(User.name.like('%test%')).all()  # Search

# Complex queries
from sqlalchemy import and_, or_
users = db.query(User).filter(
    and_(User.name == 'John', User.email.like('%@gmail.com'))
).all()
```

## 🔗 **Integration with FastAPI Endpoints**

### **Dependency Injection Pattern**
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.database import get_db

@app.get("/api/v1/users/")
async def get_users(db: Session = Depends(get_db)):
    """The db parameter automatically gets a database session"""
    return db.query(User).all()
```

**How it works:**
1. `Depends(get_db)` creates a database session
2. FastAPI automatically calls `get_db()` 
3. Session is passed to your function as `db`
4. Session is automatically closed after request

## 🎯 **Next Steps**

1. **✅ Current Status**: SQLite database working
2. **🔄 Add Models**: Create more database models as needed
3. **🚀 API Endpoints**: Create CRUD endpoints for your models  
4. **🧪 Testing**: Add database tests
5. **📊 Migration**: Consider PostgreSQL for production

Your database is **ready to use**! The SQLite setup provides a solid foundation for development and can easily be migrated to PostgreSQL or MySQL for production. 🎉
