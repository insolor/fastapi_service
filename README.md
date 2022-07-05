# inside

Run from docker (hub):
```
make run
```
Full command example:
```
docker container run -e DATABASE_URL='sqlite:///./base.db' -p 10000:10000 -t insolor/inside_test_project:latest
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
Result:
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
Result:
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
Result:
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
## Curl examples:
```curl
> curl -X 'POST' \
  'http://0.0.0.0:10000/user/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "user1",
  "password": "123"
}'

{"token":"eyJ...QzI"}

> curl -X 'POST' \
  'http://0.0.0.0:10000/user/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "user1",
  "password": "123"
}'


```