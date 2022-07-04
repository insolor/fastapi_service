from typing import List, Union

from fastapi import Body, Depends, FastAPI

from inside.auth.auth_bearer import JWTBearer
from inside.auth.auth_handler import sign_jwt
from inside.schemas import Error, Message, UserCreate

app = FastAPI()

users = []

messages = []


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserCreate = Body(...)):
    users.append(user)
    return sign_jwt(user.name)


@app.post("/user/login", tags=["user"])
def user_login(user: UserCreate = Body(...)):
    if check_user(user):
        return sign_jwt(user.name)
    return Error(error="Wrong login details!")


def check_user(data: UserCreate):
    return any(
        user.name == data.name and user.password == data.password for user in users
    )


@app.post("/messages", dependencies=[Depends(JWTBearer())], tags=["messages"])
def post_message(message: Message = Body(...)):
    command_result = get_last_messages(message)
    if command_result:
        return command_result
    else:
        messages.append(message)


def get_last_messages(
    message: Message,
) -> Union[None, Error, List[Message]]:
    command, *args = message.message.split(maxsplit=1)
    if command == "messages" and args:
        try:
            count = int(args[0])
        except Exception:
            return Error(error=f"Wrong command: {message.message!r}")

        return messages[-count:]

    return None
