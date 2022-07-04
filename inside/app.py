from fastapi import Body, FastAPI
from inside.auth.auth_handler import sign_jwt

from inside.model import UserLoginSchema, UserSchema

app = FastAPI()

users = []


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return sign_jwt(user.name)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.name)
    return {
        "error": "Wrong login details!"
    }


def check_user(data: UserLoginSchema):
    return any(user.name == data.name and user.password == data.password for user in users)
