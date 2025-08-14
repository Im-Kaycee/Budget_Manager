from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import users,budget, expenses, affordability
app = FastAPI()
# Allow CORS for all origins
app.include_router(users.router)
app.include_router(budget.router)
app.include_router(expenses.router)
app.include_router(affordability.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome"}            

'''
# Database Initialization
from database import engine
import models

def create_db():
    models.SQLModel.metadata.create_all(engine)

create_db()
'''