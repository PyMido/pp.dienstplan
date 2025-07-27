from uuid import UUID, uuid4
from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Pluspunkt Dienstplan", version="1.0.0")

# ── Modelle ─────────────────────────────────────────────────────────────────── #

class EmployeeIn(BaseModel):
    first_name: str = Field(..., example="Anna")
    last_name: str = Field(..., example="Muster")
    weekly_hours: int = Field(..., gt=0, le=40, example=32)


class Employee(EmployeeIn):
    id: UUID


# ── In-Memory-DB (später DB ersetzen) ───────────────────────────────────────── #

_db: dict[UUID, Employee] = {}

# ── CRUD-Endpunkte ─────────────────────────────────────────────────────────── #

@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(emp: EmployeeIn) -> Employee:
    new_emp = Employee(id=uuid4(), **emp.dict())
    _db[new_emp.id] = new_emp
    return new_emp


@app.get("/employees", response_model=List[Employee])
def list_employees() -> List[Employee]:
    return list(_db.values())


@app.delete("/employees/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: UUID) -> None:
    if _db.pop(emp_id, None) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
