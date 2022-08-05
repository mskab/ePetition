from db.models.complaint import Complaint
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schemas.complaint import ComplaintCreate, ComplaintUpdate
from sqlalchemy.orm import Session


def create(_db: Session, complaint: ComplaintCreate):
    try:
        db_complaint = Complaint(
            abuse=complaint.abuse,
            description=complaint.description,
            owner_id=complaint.owner_id,
            petition_id=complaint.petition_id,
        )
        _db.add(db_complaint)
        _db.commit()
        _db.refresh(db_complaint)

        return db_complaint
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from exc


def get_by_id(_db: Session, complaint_id: int):
    db_complaint = (
        _db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found with the given ID",
        )

    return db_complaint


def get_all(_db: Session, offset: int = 0, limit: int = 100):
    return _db.query(Complaint).offset(offset).limit(limit).all()


def update(_db: Session, complaint_id: int, complaint: ComplaintUpdate):
    db_complaint = get_by_id(_db, complaint_id)
    update_complaint_encode = jsonable_encoder(complaint)
    if update_complaint_encode["status"]:
        db_complaint.status = update_complaint_encode["status"]

    _db.commit()
    _db.refresh(db_complaint)

    return db_complaint


def delete(_db: Session, complaint_id: int):
    complaint = get_by_id(_db, complaint_id)
    _db.delete(complaint)
    _db.commit()
