"""
Hello World API Routes
"""
from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/hello", response_model=Dict[str, str])
async def hello_world() -> Dict[str, str]:
    """
    Returns a Hello World message
    """
    return {"message": "HELLO WORLD"}


@router.get("/hello/{name}", response_model=Dict[str, str])
async def hello_person(name: str) -> Dict[str, str]:
    """
    Returns a personalized Hello message
    """
    return {"message": f"HELLO {name.upper()}"}


@router.post("/hello", response_model=Dict[str, str])
async def hello_world_post() -> Dict[str, str]:
    """
    Returns a Hello World message via POST method
    """
    return {"message": "HELLO WORLD"}
