from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/auth")
def hello_world():
    return "<p>Hello, World!</p>"
