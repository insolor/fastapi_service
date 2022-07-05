# inside

## Endpoints:

### Create user
```http
POST /user/signup - create user
Body:
{
    "name": "user_name",
    "password": "user password"
}
Result (on success):
{
    "token": "*****"
}
```

