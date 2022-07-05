# inside

Run from docker (hub):

```
make run
```
Full command example:
```
docker container run -e DATABASE_URL='sqlite:///:memory:' -p 10000:10000 -t insolor/inside_test_project:latest
```
## Endpoints:

### Create user
```http
POST /user/signup - create user
Body:
{
    "name": "user1",
    "password": "user password"
}
Result (on success):
{
    "token": "*****"
}
```
### Login
```http
POST /user/signup - create user
Body:
{
    "name": "user1",
    "password": "user password"
}
Result (on success):
{
    "token": "*****"
}
```
### Post a message
```http
POST /messages
Body:
{
    "name": "user1",
    "message": "Some messages"
}
Result (on success):
{
    "message": "success"
}
```
### List N last messages
```http
POST /messages
Body:
{
    "name": "user1",
    "message": "messages 10"
}
Result:
[
    {
        "name": "user1",
        "message": "Some message"
    },
    ...
]
```