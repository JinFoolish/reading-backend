from fastapi import APIRouter, Depends
from app.dependencies import get_token_authorize

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_authorize)]
)

@router.get("/users/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}