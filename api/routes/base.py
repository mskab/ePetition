from fastapi import APIRouter
from routes import user, petition

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    petition.router, prefix="/petitions", tags=["petitions"])
