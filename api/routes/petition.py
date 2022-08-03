from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.petition import PetitionCreate, PetitionInfo, PetitionUpdate, PetitionSign
from db.session import get_db
from db.repository import petition

router = APIRouter()


@router.post("/", response_model=PetitionInfo, status_code=status.HTTP_201_CREATED)
def create_petition(req_petition: PetitionCreate, db: Session = Depends(get_db)):
    """
    Create a Petition and store it in the database
    """
    return petition.create(db, req_petition)


@router.get('/', response_model=List[PetitionInfo])
def get_all_petitions(db: Session = Depends(get_db)):
    """
    Get all the Petitions stored in database
    """
    return petition.get_all(db)


@router.get('/{petition_id}', response_model=PetitionInfo)
def get_petition(petition_id: int, db: Session = Depends(get_db)):
    """
    Get the Petition with the given ID
    """
    return petition.get_by_id(db, petition_id)


@router.put('/{petition_id}', response_model=PetitionInfo)
def update_petition(petition_id: int, req_petition: PetitionUpdate, db: Session = Depends(get_db)):
    """
    Update a Petition stored in the database
    """
    return petition.update(db, petition_id, req_petition)


@router.delete('/{petition_id}')
def delete_petition(petition_id: int, db: Session = Depends(get_db)):
    """
    Delete the Petition with the given ID
    """
    petition.delete(db, petition_id)

    return "Petition deleted successfully"


@router.post('/{petition_id}/sign', response_model=PetitionInfo)
def sign_petition(petition_id: int, req_petition: PetitionSign, db: Session = Depends(get_db)):
    """
    Sing a Petition stored in the database
    """
    return petition.sign_petition(db, petition_id, req_petition)
