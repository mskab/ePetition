from fastapi import APIRouter
from api.routes import auth, complaint, decision_maker, petition, user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    petition.router, prefix="/petitions", tags=["petitions"]
)
api_router.include_router(
    decision_maker.router,
    prefix="/decision_makers",
    tags=["decision_makers"],
)
api_router.include_router(
    complaint.router, prefix="/complaints", tags=["complaints"]
)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
