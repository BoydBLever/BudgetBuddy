from fastapi import FastAPI, Body, Query
from pydantic import BaseModel
from typing import List, Optional
from mcp import router as mcp_router

app = FastAPI()

app.include_router(mcp_router)

# --- Data Models ---
class BudgetData(BaseModel):
    user_id: str
    category: Optional[str] = None
    transaction_history: Optional[List[dict]] = None
    budget_limit: Optional[float] = None
    purchase_amount: Optional[float] = None
    attempt: Optional[int] = None

class BudgetResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[dict] = None

# --- API Endpoints ---
# Hackathon: Always returns a success response; FE to pass in a number for budget limit.
@app.post("/budget")
async def create_budget(budgetData: BudgetData = Body(...)) -> BudgetResponse:
    return BudgetResponse(status="success", message="Budget created.")

@app.get("/budget")
async def get_budget(
    user_id: str = Query(..., alias="user_id"),
    category: str = Query(..., alias="category"),
) -> BudgetResponse:
    # Example hardcoded demo logic
    if category.lower() == "food":
        return BudgetResponse(
            status="success",
            message=f"Budget fetched for {category}",
            data={"category": category, "limit": 200, "spent": 50}
        )
    else:
        return BudgetResponse(
            status="success",
            message=f"Budget fetched for {category}",
            data={"category": category, "limit": 100, "spent": 25}
        )

@app.get("/check_budget")
async def check_budget(budgetData: BudgetData = Body(...)) -> BudgetResponse:
    # Hardcoded values for demo
    budget_limit = 200    # Food category limit
    spent = 50            # Already spent
    purchase_amount = budgetData.purchase_amount or 0

    if budgetData.category != "food":
        return BudgetResponse(status="unsupported", message="Only food category supported in demo.")
    if spent + purchase_amount <= budget_limit:
        return BudgetResponse(status="within_budget", message=f"You CAN afford this ${purchase_amount} purchase.")
    else:
        return BudgetResponse(status="exceeds_budget", message=f"You CANNOT afford this ${purchase_amount} purchase.")

@app.post("/record_payment")
async def record_payment(budgetData: BudgetData = Body(...)) -> BudgetResponse:
    # For demo: after one $10 purchase, can't afford a second
    budget_limit = 10
    spent = 0
    # Simulate "attempt number" to differentiate calls in demo
    # On attempt 1, approve payment; on attempt 2, reject.
    if budgetData.attempt == 1 or budgetData.attempt is None:
        spent += budgetData.purchase_amount or 0
        remaining = budget_limit - spent
        return BudgetResponse(
            status="success",
            message=f"Payment recorded. Remaining budget: ${remaining}."
        )
    else:
        return BudgetResponse(
            status="exceeds_budget",
            message="Insufficient budget for this purchase."
        )

# Show API is running
@app.get("/")
async def root():
    return {"message": "Backend API is running"}
