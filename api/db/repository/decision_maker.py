from api.db.models.decision_maker import DecisionMaker
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from api.schemas.decision_maker import (
    DecisionMakerCreate,
    DecisionMakerUpdate,
)
from sqlalchemy.orm import Session


def create(_db: Session, decision_maker: DecisionMakerCreate):
    is_decision_maker_exist_by_email(_db, decision_maker.email)
    db_decision_maker = DecisionMaker(
        naming=decision_maker.naming,
        affiliation=decision_maker.affiliation,
        email=decision_maker.email,
    )
    _db.add(db_decision_maker)
    _db.commit()
    _db.refresh(db_decision_maker)

    return db_decision_maker


def is_decision_maker_exist_by_email(_db: Session, email: str):
    db_decision_maker = (
        _db.query(DecisionMaker)
        .filter(DecisionMaker.email == email)
        .first()
    )
    if db_decision_maker:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Decision maker already exists",
        )


def get_by_id(_db: Session, decision_maker_id: int):
    decision_maker = (
        _db.query(DecisionMaker)
        .filter(DecisionMaker.id == decision_maker_id)
        .first()
    )
    if not decision_maker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision maker not found with the given ID",
        )
    return decision_maker


def get_all(
    _db: Session,
    offset: int = 0,
    limit: int = 100,
    search_query: str = "",
):
    return (
        _db.query(DecisionMaker)
        .filter(
            DecisionMaker.naming.contains(search_query, autoescape=True)
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


def update(
    _db: Session,
    decision_maker_id: int,
    decision_maker: DecisionMakerUpdate,
):
    db_decision_maker = get_by_id(_db, decision_maker_id)
    update_decision_maker_encoded = jsonable_encoder(decision_maker)
    if update_decision_maker_encoded["naming"]:
        db_decision_maker.naming = update_decision_maker_encoded[
            "naming"
        ]

    if update_decision_maker_encoded["affiliation"]:
        db_decision_maker.affiliation = update_decision_maker_encoded[
            "affiliation"
        ]

    if update_decision_maker_encoded["email"]:
        db_decision_maker.email = update_decision_maker_encoded["email"]

    if update_decision_maker_encoded["is_verified"] is not None:
        db_decision_maker.is_verified = update_decision_maker_encoded[
            "is_verified"
        ]

    _db.commit()
    _db.refresh(db_decision_maker)

    return db_decision_maker


def delete(_db: Session, decision_maker_id: int):
    decision_maker = get_by_id(_db, decision_maker_id)
    _db.delete(decision_maker)
    _db.commit()
