from fastapi import FastAPI
from app.routers import books, auth, users

# Initialize FastAPI App
app = FastAPI(
    title="BookStore REST API",
    description="An asynchronous CRUD REST API with auto-generated OpenAPI documentation and Pydantic validation.",
    version="1.0.0"
)


app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router) 

@app.get("/",include_in_schema=False)
async def home():
    return {"message": "BookStore API is running.Visit /docs to test it."}
