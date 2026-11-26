from datetime import date

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from data.loans import loans
from data.members import members
from data.tools import tools

load_dotenv()

app = FastAPI()


class Tool(BaseModel):
    id: int
    name: str
    category: str
    description: str
    loan_period_days: int
    available: bool


class ToolsResponse(BaseModel):
    tools: list[Tool]


class ToolResponse(BaseModel):
    tool: Tool


class Member(BaseModel):
    id: int
    name: str
    email: str
    joined_date: str


class MembersResponse(BaseModel):
    members: list[Member]


class MemberResponse(BaseModel):
    member: Member


class Loan(BaseModel):
    id: int
    tool_id: int
    member_id: int
    borrowed_date: str
    due_date: str
    returned_date: str | None


class LoansResponse(BaseModel):
    loans: list[Loan]


# FastAPI responds 422 to an invalid request (e.g. a non-integer id) by
# default; this API uses 400 Bad Request instead.
@app.exception_handler(RequestValidationError)
def handle_validation_error(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Bad request"})


@app.get("/api/tools")
def get_tools() -> ToolsResponse:
    return {"tools": tools}


@app.get("/api/tools/{id}")
def get_tool_by_id(id: int) -> ToolResponse:
    tool = next((t for t in tools if t["id"] == id), None)
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"tool": tool}


@app.get("/api/members")
def get_members() -> MembersResponse:
    return {"members": members}


@app.get("/api/members/{id}")
def get_member_by_id(id: int) -> MemberResponse:
    member = next((m for m in members if m["id"] == id), None)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"member": member}


@app.get("/api/loans")
def get_loans() -> LoansResponse:
    return {"loans": loans}


@app.get("/api/loans/overdue")
def get_overdue_loans() -> LoansResponse:
    today = date.today().isoformat()
    overdue = [loan for loan in loans if loan["returned_date"] is None and loan["due_date"] < today]
    return {"loans": overdue}


# The week's running feature - POST /api/ask - should be added here
# then extended in place as we work through the tasks up to Day 5
