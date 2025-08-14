from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import schemas, models, auth, database
from typing import List
router = APIRouter(prefix="/budget", tags=["Budget"])
from models import User, Budget, Expense

@router.post("/set", response_model=schemas.BudgetRead)
def create_budget(budget: schemas.BudgetCreate, session: Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    existing_budget = session.exec(
        select(models.Budget).where(
            models.Budget.user_id == current_user.id,
            models.Budget.start_date <= budget.end_date,
            models.Budget.end_date >= budget.start_date
        )
    ).first()
    
    if existing_budget:
        raise HTTPException(status_code=400, detail="Budget already exists for this period")

    db_budget = models.Budget(
        user_id=current_user.id,
        amount=budget.amount,
        period=budget.period,
        start_date=budget.start_date,
        end_date=budget.end_date
    )
    
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    
    return db_budget
@router.get("/", response_model=List[schemas.BudgetRead])
def get_user_budgets(
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    budgets = session.exec(
        select(models.Budget).where(models.Budget.user_id == current_user.id)
    ).all()
    return budgets
@router.get("/{budget_id}", response_model=schemas.BudgetRead)
def get_budget(
    budget_id: int,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    budget = session.get(models.Budget, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    return budget
@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    budget = session.get(models.Budget, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    session.delete(budget)
    session.commit()
    return {"message": "Budget deleted successfully"}

@router.put("/{budget_id}", response_model=schemas.BudgetRead)
def update_budget(
    budget_id: int,
    budget: schemas.BudgetCreate,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_budget = session.get(models.Budget, budget_id)
    if not db_budget or db_budget.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    for key, value in budget.model_dump(exclude_unset=True).items():
        setattr(db_budget, key, value)

    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    
    return db_budget