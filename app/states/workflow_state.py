import reflex as rx
import uuid
import datetime
from app.models import WorkflowTemplate
from app.states.auth_state import AuthState

MOCK_WORKFLOWS: list[WorkflowTemplate] = [
    WorkflowTemplate(
        id="1",
        name="Standard Expense",
        description="Approval workflow for expenses under $1000",
        stages=["Manager", "Finance"],
        created_by="admin",
        created_date="2023-10-01",
    )
]


class WorkflowState(rx.State):
    workflows: list[WorkflowTemplate] = MOCK_WORKFLOWS
    is_creating: bool = False

    @rx.event
    def toggle_creating(self):
        self.is_creating = not self.is_creating

    @rx.event
    async def create_workflow(self, form_data: dict):
        user = await self.get_state(AuthState)
        if user.user_role != "Admin":
            return rx.toast.error("Only Admins can create workflows")
        name = form_data.get("name")
        description = form_data.get("description")
        stages_str = form_data.get("stages", "")
        if not name:
            return rx.toast.error("Workflow Name is required")
        stages = [s.strip() for s in stages_str.split(",") if s.strip()]
        new_wf = WorkflowTemplate(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            stages=stages,
            created_by=user.user.username,
            created_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        self.workflows.append(new_wf)
        self.is_creating = False
        return rx.toast.success("Workflow template created")

    @rx.event
    async def delete_workflow(self, wf_id: str):
        user = await self.get_state(AuthState)
        if user.user_role != "Admin":
            return rx.toast.error("Unauthorized")
        self.workflows = [w for w in self.workflows if w.id != wf_id]
        return rx.toast.success("Workflow deleted")