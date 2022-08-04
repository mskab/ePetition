from db.models.decision_maker import DecisionMaker
from db.models.petition import Petition
from db.models.petition_decision_maker import petition_decision_maker
from db.repository import user
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from schemas.petition import (
    PetitionCreate,
    PetitionSign,
    PetitionUpdate,
)
from sqlalchemy import and_
from sqlalchemy.orm import Session


def create(_db: Session, petition: PetitionCreate):
    db_petition = Petition(
        title=petition.title,
        description=petition.description,
        image=petition.image,
        country=petition.country,
        due_date=petition.due_date,
        signed_goal=petition.signed_goal,
        owner_id=petition.owner_id,
    )
    decision_makers = _db.query(DecisionMaker).filter(
        DecisionMaker.id.in_(petition.decision_makers)
    )
    if decision_makers.count() == len(petition.decision_makers):
        db_petition.decision_makers.extend(decision_makers)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision maker not found",
        )

    _db.add(db_petition)
    _db.commit()
    _db.refresh(db_petition)

    return db_petition


def get_by_id(_db: Session, petition_id: int, petition_status=""):
    if petition_status:
        db_petition = _db.query(Petition).filter(
            and_(
                Petition.status == petition_status,
                Petition.id == petition_id,
            )
        )
    else:
        db_petition = _db.query(Petition).filter(
            Petition.id == petition_id
        )
    if not db_petition.count():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petition not found with the given ID",
        )

    return db_petition.first()


def get_all(_db: Session, offeset: int = 0, limit: int = 100):
    return _db.query(Petition).offset(offeset).limit(limit).all()


def update(_db: Session, petition_id: int, petition: PetitionUpdate):
    db_petition = get_by_id(_db, petition_id)
    update_petition_encode = jsonable_encoder(petition)
    if update_petition_encode["due_date"]:
        db_petition.due_date = update_petition_encode["due_date"]

    if update_petition_encode["signed_goal"]:
        db_petition.signed_goal = update_petition_encode["signed_goal"]

    if update_petition_encode["status"]:
        db_petition.status = update_petition_encode["status"]

    if update_petition_encode["decision_makers"]:
        decision_makers = _db.query(DecisionMaker).filter(
            DecisionMaker.id.in_(petition.decision_makers)
        )
        if decision_makers.count() == len(petition.decision_makers):
            removed_decision_makers = (
                petition_decision_maker.delete().where(
                    petition_decision_maker.c.decision_maker_id.not_in(
                        petition.decision_makers
                    )
                    & (
                        petition_decision_maker.c.petition_id
                        == db_petition.id
                    )
                )
            )

            _db.execute(removed_decision_makers)
            _db.commit()

            db_petition.decision_makers.extend(decision_makers)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision maker not found",
            )

    _db.commit()
    _db.refresh(db_petition)

    return db_petition


def delete(_db: Session, petition_id: int):
    petition = get_by_id(_db, petition_id)
    _db.delete(petition)
    _db.commit()


def sign_petition(
    _db: Session, petition_id: int, petition: PetitionSign
):
    db_petition = get_by_id(_db, petition_id, "active")
    supporter = user.get_by_id(_db, petition.supporter_id)
    if supporter in db_petition.supporters:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already signed petition",
        )

    db_petition.supporters.append(supporter)
    _db.commit()
    _db.refresh(db_petition)

    return db_petition
