import reflex as rx
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password_hash: str
    role: str = "Employee"
    created_at: str = ""


class Document(BaseModel):
    id: str
    title: str
    file_path: str
    file_type: str
    uploaded_by: str
    upload_date: str
    status: str = "Pending"
    reviewer: str = ""
    review_date: str = ""
    comments: str = ""


class LeaveRequest(BaseModel):
    id: str
    employee_username: str
    employee_email: str
    leave_type: str
    start_date: str
    end_date: str
    days_count: int
    reason: str
    status: str = "Pending"
    manager_comment: str = ""
    submitted_date: str
    reviewed_date: str = ""
    reviewed_by: str = ""


class GeneralRequest(BaseModel):
    id: str
    title: str
    type: str
    amount: float = 0.0
    description: str
    submitted_by: str
    submitted_date: str
    status: str = "Pending"
    priority: str = "Medium"
    approver: str = ""
    approved_date: str = ""
    rejection_reason: str = ""


class Notification(BaseModel):
    id: str
    user_username: str
    title: str
    message: str
    type: str = "Info"
    is_read: bool = False
    created_at: str
    link: str = ""


class WorkflowTemplate(BaseModel):
    id: str
    name: str
    description: str
    stages: list[str] = []
    created_by: str
    created_date: str