from fastapi import FastAPI
from app.api.endpoints import router as notion_router

app = FastAPI()

app.include_router(notion_router, prefix="/api")

@app.get("/api")
def read_root():
    return {"message": "Welcome to the Notion API"}