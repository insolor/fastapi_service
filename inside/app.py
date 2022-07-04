from typing import List, Union

from fastapi import Body, Depends, FastAPI

from inside.auth.auth_bearer import JWTBearer
from inside.auth.auth_handler import sign_jwt
from inside.model import Error, MessageSchema, UserLoginSchema, UserSchema

app = FastAPI()

users = []

messages = []


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return sign_jwt(user.name)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.name)
    return Error(error="Wrong login details!")


def check_user(data: UserLoginSchema):
    return any(
        user.name == data.name and user.password == data.password for user in users
    )


@app.post("/messages", dependencies=[Depends(JWTBearer())], tags=["messages"])
def post_message(message: MessageSchema = Body(...)):
    command_result = get_last_messages(message)
    if command_result:
        return command_result
    else:
        messages.append(message)


def get_last_messages(
    message: MessageSchema,
) -> Union[None, Error, List[MessageSchema]]:
    command, *args = message.message.split(maxsplit=1)
    if command == "messages" and args:
        try:
            count = int(args[0])
        except Exception:
            return Error(error=f"Wrong command: {message.message!r}")

        return messages[-count:]

    return None
