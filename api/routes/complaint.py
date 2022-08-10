from typing import List

from db.repository import auth, complaint
from db.session import get_db
from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from schemas.common import StatusResponse
from schemas.complaint import (
    ComplaintCreate,
    ComplaintInfo,
    ComplaintUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter()
default_session = Depends(get_db)
default_authJWT = Depends()


@router.post(
    "/",
    response_model=ComplaintInfo,
    status_code=status.HTTP_201_CREATED,
)
def create_complaint(
    req_complaint: ComplaintCreate,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Create a Complaint and store it in the database
    """
    auth.is_only_user_permitted(db, Auth)

    return complaint.create(db, req_complaint)


@router.get("/", response_model=List[ComplaintInfo])
def get_all_complaints(
    offset: int,
    limit: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Get all the Complaints stored in database
    """
    auth.is_only_admin_permitted(db, Auth)

    return complaint.get_all(db, offset, limit)


@router.get("/{complaint_id}", response_model=ComplaintInfo)
def get_complaint(
    complaint_id: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Get the Complaint with the given ID
    """
    auth.is_only_admin_permitted(db, Auth)

    return complaint.get_by_id(db, complaint_id)


@router.put("/{complaint_id}", response_model=ComplaintInfo)
def update_complaint(
    complaint_id: int,
    req_complaint: ComplaintUpdate,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Update a Complaint stored in the database
    """
    auth.is_only_admin_permitted(db, Auth)

    return complaint.update(db, complaint_id, req_complaint)


@router.delete("/{complaint_id}", response_model=StatusResponse)
def delete_complaint(
    complaint_id: int,
    db: Session = default_session,
    Auth: AuthJWT = default_authJWT,
):
    """
    Delete the Complaint with the given ID
    """
    auth.is_only_admin_permitted(db, Auth)
    complaint.delete(db, complaint_id)

    return {
        "success": True,
        "message": "Complaint deleted successfully",
    }
