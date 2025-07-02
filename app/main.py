from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="My FastAPI App", version="1.0.0")

class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get("/")
async def root():
    return {"message": "Hello, Wordl!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}