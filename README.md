# Budget Tracker API

A FastAPI-powered backend for a personal budget tracking application with JWT authentication.

## Features

- **User Authentication** (JWT tokens)
- **Budget Management** (Create, Read, Update, Delete)
- **Expense Tracking** with categories
- **Analytics** (Weekly/Monthly spending reports)
- **Budget vs Spending Comparison**

## API Endpoints

### 🔐 Authentication (`/users`)

| Method | Endpoint       | Description                     | Request Body                              |
|--------|----------------|---------------------------------|------------------------------------------|
| POST   | `/users/register` | Register new user              | `{username, email, password}`           |
| POST   | `/users/login`    | Login (get JWT token)          | `{username, password}` (form-urlencoded) |
| GET    | `/users/me`       | Get current user details       | Requires JWT in header                  |

### 💰 Budget Management (`/budget`)

| Method | Endpoint            | Description                     | Request Body                              |
|--------|---------------------|---------------------------------|------------------------------------------|
| POST   | `/budget/set`       | Create new budget               | `{amount, period, start_date, end_date}`|
| GET    | `/budget/`          | List all user budgets           | -                                        |
| GET    | `/budget/{budget_id}`| Get specific budget            | -                                        |
| PUT    | `/budget/{budget_id}`| Update budget                  | Same as POST                             |
| DELETE | `/budget/{budget_id}`| Delete budget                  | -                                        |

### 💸 Expense Tracking (`/expenses`)

| Method | Endpoint              | Description                     | Request Body                              |
|--------|-----------------------|---------------------------------|------------------------------------------|
| POST   | `/expenses/`          | Create new expense              | `{amount, category, date, description}` |
| GET    | `/expenses/`          | List all expenses               | -                                        |
| GET    | `/expenses/{expense_id}`| Get specific expense          | -                                        |
| DELETE | `/expenses/{expense_id}`| Delete expense                | -                                        |

### 📊 Analytics

| Method | Endpoint                     | Description                     | Query Params             |
|--------|------------------------------|---------------------------------|--------------------------|
| GET    | `/expenses/analysis/weekly`  | Weekly spending report         | `weeks_ago` (default: 0)|
| GET    | `/expenses/analysis/monthly` | Monthly spending report        | `months_ago` (default: 0)|
| GET    | `/expenses/analysis/compare` | Compare spending vs budget     | -                        |

## Setup Guide

### Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the server:
   ```bash
   uvicorn main:app --reload
3. Access the Docs:
   http://localhost:8000/docs
