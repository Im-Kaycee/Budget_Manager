from pydantic import BaseModel
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    date: datetime
    category:str
    
class ExpenseRead(BaseModel):
    id: int
    amount: float
    description: str | None
    date: datetime
    category: str

    class Config:
        orm_mode = True
class BudgetCreate(BaseModel):
    amount:float
    period:str
    start_date:datetime
    end_date: datetime
    
class BudgetRead(BaseModel):
    id: int
    amount: float
    period: str
    start_date: datetime
    end_date: datetime
    
    class Config:
        orm_mode = True