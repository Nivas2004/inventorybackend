from fastapi import APIRouter, HTTPException
from app.schemas import User
from app.database import users_collection

router = APIRouter()

# 🔹 Register API
@router.post("/register")
async def register(user: User):
    existing = await users_collection.find_one({"username": user.username})

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = user.dict()
    await users_collection.insert_one(new_user)

    return {"success": True, "message": "User registered successfully"}

# 🔹 Login API
@router.post("/login")
async def login(user: User):
    existing = await users_collection.find_one({"username": user.username})

    if existing and existing["password"] == user.password:
        return {"success": True, "message": "Login successful"}
    
    raise HTTPException(status_code=400, detail="Invalid username or password")
