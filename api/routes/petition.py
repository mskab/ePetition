from typing import List

from api.db.repository import auth, petition
from api.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from api.schemas.common import StatusResponse
from api.schemas.petition import (
    PetitionCreate,
    PetitionInfo,
    PetitionSign,
    PetitionUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter()
default_session = Depends(get_db)
default_authJWT = Depends()


@router.post(
    "/",
    response_model=PetitionInfo,
    status_code=status.HTTP_201_CREATED,
)
def create_petition(
    req_petition: PetitionCreate,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Create a Petition and store it in the database
    """
    auth.is_only_user_permitted(db, Auth)

    return petition.create(db, req_petition)


@router.get("/", response_model=List[PetitionInfo])
def get_all_petitions(
    db: Session = default_session,
    limit: int = 100,
    offset: int = 0,
    ordering: str = None,
    statuses: str = None,
    creation_date: str = None,
    due_date: str = None,
):
    """
    Get all the Petitions stored in database
    """
    if ordering:
        ordering = ordering.split(",")

    if statuses:
        statuses = statuses.split(",")

    if creation_date:
        creation_date = creation_date.split(",")

    if due_date:
        due_date = due_date.split(",")

    return petition.get_all(
        db, offset, limit, statuses, creation_date, due_date, ordering
    )


@router.get("/search", response_model=List[PetitionInfo])
def search_petitions(
    db: Session = default_session,
    limit: int = 100,
    offset: int = 0,
    q: str = "",
    ordering: str = None,
    statuses: str = None,
    creation_date: str = None,
    due_date: str = None,
):
    """
    Search petitions by requested query
    """
    if ordering:
        ordering = ordering.split(",")

    if statuses:
        statuses = statuses.split(",")

    if creation_date:
        creation_date = creation_date.split(",")

    if due_date:
        due_date = due_date.split(",")

    return petition.get_all(
        db,
        offset,
        limit,
        statuses,
        creation_date,
        due_date,
        ordering,
        q,
    )


@router.get("/{petition_id}", response_model=PetitionInfo)
def get_petition(petition_id: int, db: Session = default_session):
    """
    Get the Petition with the given ID
    """
    return petition.get_by_id(db, petition_id)


@router.put("/{petition_id}", response_model=PetitionInfo)
def update_petition(
    petition_id: int,
    req_petition: PetitionUpdate,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Update a Petition stored in the database
    """
    current_user = auth.get_authenteficated_user(db, Auth)

    if not current_user.is_admin and req_petition.status not in [
        "victory",
        "closed",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Update status not allowed",
        )
    return petition.update(db, petition_id, req_petition, current_user)


@router.delete("/{petition_id}", response_model=StatusResponse)
def delete_petition(
    petition_id: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Delete the Petition with the given ID
    """
    auth.is_only_admin_permitted(db, Auth)
    petition.delete(db, petition_id)

    return {"success": True, "message": "Petition deleted successfully"}


@router.post("/{petition_id}/sign", response_model=PetitionInfo)
def sign_petition(
    petition_id: int,
    req_petition: PetitionSign,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Sign a Petition stored in the database
    """
    auth.is_only_user_permitted(db, Auth)

    return petition.sign_petition(db, petition_id, req_petition)
