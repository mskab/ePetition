from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.complaint import ComplaintCreate, ComplaintInfo, ComplaintUpdate
from db.session import get_db
from db.repository import complaint as repo

router = APIRouter()


@router.post("/", response_model=ComplaintInfo, status_code=status.HTTP_201_CREATED)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    """
    Create a Complaint and store it in the database
    """
    return repo.create(db, complaint)


@router.get('/', response_model=List[ComplaintInfo])
def get_all_complaints(db: Session = Depends(get_db)):
    """
    Get all the Complaints stored in database
    """
    return repo.get_all(db)


@router.get('/{petition_id}', response_model=ComplaintInfo)
def get_complaint(petition_id: int, db: Session = Depends(get_db)):
    """
    Get the Complaint with the given ID
    """
    return repo.get_by_id(db, petition_id)


@router.put('/{petition_id}', response_model=ComplaintInfo)
def update_complaint(petition_id: int, petition: ComplaintUpdate, db: Session = Depends(get_db)):
    """
    Update a Complaint stored in the database
    """
    return repo.update(db, petition_id, petition)


@router.delete('/{petition_id}')
def delete_complaint(petition_id: int, db: Session = Depends(get_db)):
    """
    Delete the Complaint with the given ID
    """
    repo.delete(db, petition_id)

    return "Complaint deleted successfully"
