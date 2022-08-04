from sqlalchemy.orm import Session
from schemas.decision_maker import DecisionMakerCreate, DecisionMakerUpdate
from db.models.decision_maker import DecisionMaker
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder


def create(db: Session, decision_maker: DecisionMakerCreate):
    is_decision_maker_exist_by_email(db, decision_maker.email)
    db_decision_maker = DecisionMaker(
        naming=decision_maker.naming,
        affiliation=decision_maker.affiliation,
        email=decision_maker.email,
    )
    db.add(db_decision_maker)
    db.commit()
    db.refresh(db_decision_maker)

    return db_decision_maker


def is_decision_maker_exist_by_email(db: Session, email: str):
    db_decision_maker = (
        db.query(DecisionMaker).filter(DecisionMaker.email == email).first()
    )
    if db_decision_maker:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Decision maker already exists",
        )


def get_by_id(db: Session, decision_maker_id: int):
    decision_maker = (
        db.query(DecisionMaker)
        .filter(DecisionMaker.id == decision_maker_id)
        .first()
    )
    if not decision_maker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision maker not found with the given ID",
        )
    return decision_maker


def get_all(db: Session, offset: int = 0, limit: int = 100):
    return db.query(DecisionMaker).offset(offset).limit(limit).all()


def update(
    db: Session, decision_maker_id: int, decision_maker: DecisionMakerUpdate
):
    db_decision_maker = get_by_id(db, decision_maker_id)
    update_user_encoded = jsonable_encoder(decision_maker)
    if update_user_encoded["naming"]:
        db_decision_maker.naming = update_user_encoded["naming"]

    if update_user_encoded["affiliation"]:
        db_decision_maker.affiliation = update_user_encoded["affiliation"]

    if update_user_encoded["email"]:
        db_decision_maker.email = update_user_encoded["email"]

    db.commit()
    db.refresh(db_decision_maker)

    return db_decision_maker


def delete(db: Session, decision_maker_id: int):
    decision_maker = get_by_id(db, decision_maker_id)
    db.delete(decision_maker)
    db.commit()
