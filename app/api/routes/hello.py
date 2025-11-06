"""
Hello World API Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db, User

router = APIRouter()


@router.get("/hello", response_model=dict[str, str])
async def hello_world() -> dict[str, str]:
    """
    Returns a Hello World message
    """
    return {"message": "HELLO WORLD, This is a sample GET method"}


@router.get("/hello/{name}", response_model=dict[str, str])
async def hello_person(name: str) -> dict[str, str]:
    """
    Returns a personalized Hello message
    """
    return {"message": f"HELLO {name.upper()}"}


@router.post("/hello", response_model=dict[str, str])
async def hello_world_post() -> dict[str, str]:
    """
    Returns a Hello World message via POST method
    """
    return {"message": "HELLO WORLD"}


@router.get("/database-info")
async def get_database_info(db: Session = Depends(get_db)):
    """Get database connection information"""
    try:
        user_count = db.query(User).count()
        users = db.query(User).all()
        
        user_list = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
        
        return {
            "database_type": "SQLite",
            "connection_status": "Connected", 
            "total_users": user_count,
            "users": user_list
        }
    except Exception as e:
        return {"connection_status": "Error", "error": str(e)}
