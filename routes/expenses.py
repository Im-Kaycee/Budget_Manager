from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
import schemas, models, auth, database
from typing import List
router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=schemas.ExpenseRead)
def create_expense(expense: schemas.ExpenseCreate, session: Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    db_expense = models.Expense(
        user_id=current_user.id,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        description=expense.description
    )
    
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    
    return db_expense

@router.get("/", response_model = List[schemas.ExpenseRead])
def get_expenses(
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    expenses = session.exec(
        select(models.Expense).where(models.Expense.user_id == current_user.id)
    ).all()
    return expenses
@router.get("/{expense_id}", response_model=schemas.ExpenseRead)
def get_expense(
    expense_id: int,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    expense = session.get(models.Expense, expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
):
    expense = session.get(models.Expense, expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")

    session.delete(expense)
    session.commit()
    return {"message": "Expense deleted successfully"}
from datetime import datetime, timedelta
from fastapi import Query

@router.get("/analysis/weekly")
def weekly_analysis(
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
    weeks_ago: int = Query(0, ge=0)
):
    end_date = datetime.now() - timedelta(weeks=weeks_ago*7)
    start_date = end_date - timedelta(days=7)
    
    expenses = session.exec(
        select(models.Expense).where(
            models.Expense.user_id == current_user.id,
            models.Expense.date >= start_date,
            models.Expense.date <= end_date
        )
    ).all()
    
    return {
        "period": f"Week {end_date.isocalendar()[1]}",
        "start_date": start_date,
        "end_date": end_date,
        "total_spent": sum(e.amount for e in expenses),
        "expenses": expenses
    }

@router.get("/analysis/monthly")
def monthly_analysis(
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user),
    months_ago: int = Query(0, ge=0)
):
    end_date = datetime.now() - timedelta(days=30*months_ago)
    start_date = end_date.replace(day=1)
    
    expenses = session.exec(
        select(models.Expense).where(
            models.Expense.user_id == current_user.id,
            models.Expense.date >= start_date,
            models.Expense.date <= end_date
        )
    ).all()
    
    return {
        "period": start_date.strftime("%B %Y"),
        "start_date": start_date,
        "end_date": end_date,
        "total_spent": sum(e.amount for e in expenses),
        "expenses": expenses
    }
    
@router.get("/analysis/compare")
def compare_to_budget(
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(auth.get_current_user)
):
    now = datetime.now()
    current_month = now.replace(day=1)
    
    # Get monthly expenses
    expenses = session.exec(
        select(models.Expense).where(
            models.Expense.user_id == current_user.id,
            models.Expense.date >= current_month,
            models.Expense.date <= now
        )
    ).all()
    
    # Get current month's budget
    budget = session.exec(
        select(models.Budget).where(
            models.Budget.user_id == current_user.id,
            models.Budget.period == "monthly",
            models.Budget.start_date <= now,
            models.Budget.end_date >= now
        )
    ).first()
    
    total_spent = sum(e.amount for e in expenses)
    
    return {
        "period": current_month.strftime("%B %Y"),
        "total_spent": total_spent,
        "budget": budget.amount if budget else None,
        "remaining": (budget.amount - total_spent) if budget else None
    }