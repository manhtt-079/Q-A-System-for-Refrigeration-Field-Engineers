from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import qa_router

router = APIRouter()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(qa_router)

app.include_router(
    router,
    prefix="",
    tags=["root"]
)


@app.get("/")
async def home():
    return {"message": "Home page!"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8004)
