from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.decision_maker import DecisionMakerCreate, DecisionMakerInfo, DecisionMakerUpdate
from db.session import get_db
from db.repository import decision_maker

router = APIRouter()


@router.post("/", response_model=DecisionMakerInfo, status_code=status.HTTP_201_CREATED)
def create_decision_maker(req_decision_maker: DecisionMakerCreate, db: Session = Depends(get_db)):
    """
    Create a Decision maker and store it in the database
    """
    return decision_maker.create(db, req_decision_maker)


@router.get('/', response_model=List[DecisionMakerInfo])
def get_all_decision_makers(db: Session = Depends(get_db)):
    """
    Get all the Decision makers stored in database
    """
    return decision_maker.get_all(db)


@router.get('/{decision_maker_id}', response_model=DecisionMakerInfo)
def get_decision_maker(decision_maker_id: int, db: Session = Depends(get_db)):
    """
    Get the Decision maker with the given ID
    """
    return decision_maker.get_by_id(db, decision_maker_id)


@router.put('/{decision_maker_id}', response_model=DecisionMakerInfo)
def update_decision_maker(decision_maker_id: int, req_decision_maker: DecisionMakerUpdate, db: Session = Depends(get_db)):
    """
    Update a Decision maker stored in the database
    """
    return decision_maker.update(db, decision_maker_id, req_decision_maker)


@router.delete('/{decision_maker_id}')
def delete_decision_maker(decision_maker_id: int, db: Session = Depends(get_db)):
    """
    Delete the Decision maker with the given ID
    """
    decision_maker.delete(db, decision_maker_id)

    return "Decision maker deleted successfully"
