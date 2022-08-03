from fastapi import APIRouter
from routes import user, petition, decision_maker

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    petition.router, prefix="/petitions", tags=["petitions"])
api_router.include_router(decision_maker.router,
                          prefix="/decision_makers", tags=["decision_makers"])
