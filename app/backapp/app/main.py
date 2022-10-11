from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from time import sleep


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/items")
async def root():
    return  [
        {"name": "name 1",
        "id": 1}
    ]
