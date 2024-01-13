from fastapi import FastAPI
from routers.auth import router as auth_router
import uvicorn
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def read_root():
    return "Server is running."

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=int(environ.get("PORT", 8000)),
        reload=environ.get("RELOAD", False),
        server_header=False,
    )