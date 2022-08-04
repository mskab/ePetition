from sqlalchemy.orm import Session
from schemas.complaint import ComplaintCreate, ComplaintUpdate
from db.models.complaint import Complaint
from fastapi.encoders import jsonable_encoder
from fastapi import status, HTTPException


def create(db: Session, complaint: ComplaintCreate):
    try:
        db_complaint = Complaint(
            abuse=complaint.abuse,
            description=complaint.description,
            owner_id=complaint.owner_id,
            petition_id=complaint.petition_id,
        )
        db.add(db_complaint)
        db.commit()
        db.refresh(db_complaint)

        return db_complaint
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_by_id(db: Session, complaint_id: int):
    db_complaint = (
        db.query(Complaint).filter(Complaint.id == complaint_id).first()
    )
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found with the given ID",
        )

    return db_complaint


def get_all(db: Session, offset: int = 0, limit: int = 100):
    return db.query(Complaint).offset(offset).limit(limit).all()


def update(db: Session, complaint_id: int, complaint: ComplaintUpdate):
    db_complaint = get_by_id(db, complaint_id)
    update_complaint_encode = jsonable_encoder(complaint)
    if update_complaint_encode["status"]:
        db_complaint.status = update_complaint_encode["status"]

    db.commit()
    db.refresh(db_complaint)

    return db_complaint


def delete(db: Session, complaint_id: int):
    complaint = get_by_id(db, complaint_id)
    db.delete(complaint)
    db.commit()
