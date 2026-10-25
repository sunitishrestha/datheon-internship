from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# Initialize FastAPI App
app = FastAPI(
    title="BookStore REST API",
    description="An asynchronous CRUD REST API with auto-generated OpenAPI documentation and Pydantic validation.",
    version="1.0.0"
)

app.include_router(books.router)

@app.get("/",include_in_schema=False)
async def home():
    return {"message": "BookStore API is running.Visit /docs to test it."}
