from typing import List, Union, Optional

from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from inside import crud
from inside.auth.auth_bearer import JWTBearer
from inside.auth.auth_handler import sign_jwt
from inside.database import Base, engine, get_db
from inside.schemas import Message, UserWithPassword, Result, TokenResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/user/signup", tags=["user"])
def create_user(
    user: UserWithPassword = Body(...), db: Session = Depends(get_db)
) -> TokenResponse:
    db_user = crud.get_user_by_name(db, user.name)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    if not user.password:
        raise HTTPException(status_code=400, detail="Empty password is forbidden")

    crud.create_user(db, user)
    return TokenResponse(token=sign_jwt(user.name))


@app.post("/user/login", tags=["user"])
def user_login(
    user: UserWithPassword = Body(...), db: Session = Depends(get_db)
) -> TokenResponse:
    if crud.check_user(db, user):
        return TokenResponse(token=sign_jwt(user.name))
    raise HTTPException(status_code=403, detail="Wrong login details!")


@app.post("/messages", dependencies=[Depends(JWTBearer())], tags=["messages"])
def post_message(
    message: Message = Body(...), db: Session = Depends(get_db)
) -> Union[List[Message], Result]:
    command_result = check_command(db, message)
    if command_result:
        return command_result
    else:
        crud.post_message(db, message)
        return Result(message="success")


def check_command(db: Session, message: Message) -> Optional[List[Message]]:
    command, *args = message.message.split(maxsplit=1)
    if command == "messages" and args:
        try:
            count = int(args[0])
        except Exception:
            raise HTTPException(
                status_code=400, detail=f"Wrong command: {message.message!r}"
            )

        return crud.get_last_messages(db, count)

    return None
