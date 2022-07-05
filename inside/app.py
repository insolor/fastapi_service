from typing import List, Union

from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from inside import crud
from inside.auth.auth_bearer import JWTBearer
from inside.auth.auth_handler import sign_jwt
from inside.database import Base, SessionLocal, engine
from inside.schemas import Error, Message, UserCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return sign_jwt(user.name)


@app.post("/user/login", tags=["user"])
def user_login(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    if crud.check_user(db, user):
        return sign_jwt(user.name)
    return Error(error="Wrong login details!")


@app.post("/messages", dependencies=[Depends(JWTBearer())], tags=["messages"])
def post_message(message: Message = Body(...), db: Session = Depends(get_db)):
    command_result = get_last_messages(db, message)
    if command_result:
        return command_result
    else:
        crud.post_message(db, message)


def get_last_messages(
    db: Session,
    message: Message,
) -> Union[None, Error, List[Message]]:
    command, *args = message.message.split(maxsplit=1)
    if command == "messages" and args:
        try:
            count = int(args[0])
        except Exception:
            return Error(error=f"Wrong command: {message.message!r}")

        return crud.get_last_messages(db, count)

    return None
