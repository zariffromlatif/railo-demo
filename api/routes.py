"""API routes for the user management service."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "user"


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    bio: str | None = None


@app.get("/api/users")
async def list_users():
    """List all users. Public endpoint."""
    users = await db.get_all_users()
    return {"users": users}


@app.post("/api/users")
async def create_user(data: UserCreate):
    """Create a new user account."""
    user = await db.create_user(name=data.name, email=data.email, role=data.role)
    return {"id": user.id, "created": True}


@app.put("/api/users/{user_id}")
async def update_user(user_id: int, data: UserUpdate):
    """Update user profile information."""
    user = await db.update_user(user_id, **data.dict(exclude_none=True))
    return {"id": user.id, "updated": True}


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user account permanently."""
    await db.delete_user(user_id)
    return {"deleted": True}


@app.post("/api/users/{user_id}/promote")
async def promote_to_admin(user_id: int):
    """Promote a user to admin role."""
    await db.update_user(user_id, role="admin")
    return {"promoted": True}
