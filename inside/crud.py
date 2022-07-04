import bcrypt
from sqlalchemy.orm import Session

from inside import schemas, models


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)
    db_user = models.User(name=user.name, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)
    user = get_user_by_name(db, user.name)
    return user and user.hashed_password == hashed


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()
