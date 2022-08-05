from typing import List

from db.repository import complaint
from db.session import get_db
from fastapi import APIRouter, Depends, status
from schemas.complaint import (
    ComplaintCreate,
    ComplaintInfo,
    ComplaintUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter()
default_session = Depends(get_db)


@router.post(
    "/",
    response_model=ComplaintInfo,
    status_code=status.HTTP_201_CREATED,
)
def create_complaint(
    req_complaint: ComplaintCreate, _db: Session = default_session
):
    """
    Create a Complaint and store it in the database
    """
    return complaint.create(_db, req_complaint)


@router.get("/", response_model=List[ComplaintInfo])
def get_all_complaints(
    offset: int, limit: int, _db: Session = default_session
):
    """
    Get all the Complaints stored in database
    """
    return complaint.get_all(_db, offset, limit)


@router.get("/{complaint_id}", response_model=ComplaintInfo)
def get_complaint(complaint_id: int, _db: Session = default_session):
    """
    Get the Complaint with the given ID
    """
    return complaint.get_by_id(_db, complaint_id)


@router.put("/{complaint_id}", response_model=ComplaintInfo)
def update_complaint(
    complaint_id: int,
    req_complaint: ComplaintUpdate,
    _db: Session = default_session,
):
    """
    Update a Complaint stored in the database
    """
    return complaint.update(_db, complaint_id, req_complaint)


@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, _db: Session = default_session):
    """
    Delete the Complaint with the given ID
    """
    complaint.delete(_db, complaint_id)

    return "Complaint deleted successfully"
