import reflex as rx
import uuid
import datetime
from app.models import GeneralRequest
from app.states.auth_state import AuthState
from app.states.notification_state import NotificationState
from app.services.telegram_service import TelegramService

MOCK_REQUESTS: list[GeneralRequest] = []


class RequestState(rx.State):
    requests: list[GeneralRequest] = MOCK_REQUESTS
    filter_status: str = "All"
    filter_type: str = "All"

    @rx.var
    def filtered_requests(self) -> list[GeneralRequest]:
        filtered = self.requests
        if self.filter_status != "All":
            filtered = [r for r in filtered if r.status == self.filter_status]
        if self.filter_type != "All":
            filtered = [r for r in filtered if r.type == self.filter_type]
        return sorted(filtered, key=lambda x: x.submitted_date, reverse=True)

    @rx.event
    def set_status_filter(self, status: str):
        self.filter_status = status

    @rx.event
    def set_type_filter(self, type_val: str):
        self.filter_type = type_val

    @rx.event
    async def submit_request(self, form_data: dict):
        user = await self.get_state(AuthState)
        if not user.user:
            return rx.toast.error("Unauthorized")
        title = form_data.get("title")
        req_type = form_data.get("type")
        amount = form_data.get("amount", "0")
        description = form_data.get("description")
        priority = form_data.get("priority", "Medium")
        if not title or not description:
            return rx.toast.error("Title and Description are required")
        new_req = GeneralRequest(
            id=str(uuid.uuid4()),
            title=title,
            type=req_type,
            amount=float(amount) if amount else 0.0,
            description=description,
            priority=priority,
            submitted_by=user.user.username,
            submitted_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            status="Pending",
        )
        self.requests.insert(0, new_req)
        notif_state = await self.get_state(NotificationState)
        await notif_state.add_notification(
            user.user.username,
            "Request Submitted",
            f"Your request '{title}' has been submitted successfully.",
            "Success",
        )
        await notif_state.add_notification(
            "admin",
            "New Request",
            f"{user.user.username} submitted a new {req_type} request.",
            "Info",
        )
        msg = f"💰 New General Request\nUser: {user.user.username}\nTitle: {title}\nType: {req_type}\nAmount: ${amount}"
        if await TelegramService.send_message(msg):
            notif_state.log_telegram_message(msg)
        return rx.toast.success("Request submitted successfully")

    @rx.event
    async def approve_request(self, req_id: str):
        user = await self.get_state(AuthState)
        if user.user_role not in ["Admin", "Manager"]:
            return rx.toast.error("Unauthorized")
        for req in self.requests:
            if req.id == req_id:
                req.status = "Approved"
                req.approver = user.user.username
                req.approved_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                notif_state = await self.get_state(NotificationState)
                await notif_state.add_notification(
                    req.submitted_by,
                    "Request Approved",
                    f"Your request '{req.title}' has been approved by {user.user.username}.",
                    "Success",
                )
                msg = f"✅ Request Approved\nRequest: {req.title}\nAmount: ${req.amount}\nApprover: {user.user.username}"
                if await TelegramService.send_message(msg):
                    notif_state.log_telegram_message(msg)
                return rx.toast.success("Request approved")

    @rx.event
    async def reject_request(self, req_id: str):
        user = await self.get_state(AuthState)
        if user.user_role not in ["Admin", "Manager"]:
            return rx.toast.error("Unauthorized")
        for req in self.requests:
            if req.id == req_id:
                req.status = "Rejected"
                req.approver = user.user.username
                req.approved_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                notif_state = await self.get_state(NotificationState)
                await notif_state.add_notification(
                    req.submitted_by,
                    "Request Rejected",
                    f"Your request '{req.title}' has been rejected by {user.user.username}.",
                    "Error",
                )
                msg = f"❌ Request Rejected\nRequest: {req.title}\nAmount: ${req.amount}\nApprover: {user.user.username}"
                if await TelegramService.send_message(msg):
                    notif_state.log_telegram_message(msg)
                return rx.toast.success("Request rejected")