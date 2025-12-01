import reflex as rx
import datetime
import uuid
import logging
from app.models import LeaveRequest
from app.states.auth_state import AuthState
from app.services.telegram_service import TelegramService

MOCK_LEAVE_REQUESTS: list[LeaveRequest] = []


class LeaveState(rx.State):
    requests: list[LeaveRequest] = MOCK_LEAVE_REQUESTS
    start_date: str = datetime.date.today().strftime("%Y-%m-%d")
    end_date: str = datetime.date.today().strftime("%Y-%m-%d")
    leave_type: str = "Annual"
    reason: str = ""
    manager_comment_input: dict[str, str] = {}

    @rx.var
    def my_requests(self) -> list[LeaveRequest]:
        return self.requests

    @rx.event
    def set_manager_comment(self, request_id: str, value: str):
        self.manager_comment_input[request_id] = value

    @rx.event
    async def submit_request(self, form_data: dict):
        user = await self.get_state(AuthState)
        if not user.user:
            return rx.toast.error("Must be logged in")
        start = form_data.get("start_date")
        end = form_data.get("end_date")
        reason = form_data.get("reason")
        l_type = form_data.get("leave_type")
        if not start or not end or (not reason):
            return rx.toast.error("All fields are required")
        try:
            d1 = datetime.datetime.strptime(start, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(end, "%Y-%m-%d")
            delta = (d2 - d1).days + 1
            if delta <= 0:
                return rx.toast.error("End date must be after start date")
        except ValueError as e:
            logging.exception(f"Error: {e}")
            return rx.toast.error("Invalid date format")
        new_req = LeaveRequest(
            id=str(uuid.uuid4()),
            employee_username=user.user.username,
            employee_email=user.user.email,
            leave_type=l_type,
            start_date=start,
            end_date=end,
            days_count=delta,
            reason=reason,
            status="Pending",
            submitted_date=datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        self.requests.insert(0, new_req)
        self.reason = ""
        msg = f"📅 New Leave Request\nUser: {user.user.username}\nType: {l_type}\nDuration: {delta} days\nDates: {start} to {end}"
        if await TelegramService.send_message(msg):
            from app.states.notification_state import NotificationState

            notif_state = await self.get_state(NotificationState)
            notif_state.log_telegram_message(msg)
        return rx.toast.success("Leave request submitted")

    @rx.event
    async def approve_request(self, req_id: str):
        user = await self.get_state(AuthState)
        if user.user_role not in ["Admin", "Manager"]:
            return rx.toast.error("Unauthorized")
        comment = self.manager_comment_input.get(req_id, "")
        for req in self.requests:
            if req.id == req_id:
                req.status = "Approved"
                req.reviewed_by = user.user.username
                req.reviewed_date = datetime.datetime.now().strftime("%Y-%m-%d")
                req.manager_comment = comment
                msg = f"✅ Leave Request Approved\nEmployee: {req.employee_username}\nType: {req.leave_type}\nReviewed by: {user.user.username}"
                if await TelegramService.send_message(msg):
                    from app.states.notification_state import NotificationState

                    notif_state = await self.get_state(NotificationState)
                    notif_state.log_telegram_message(msg)
                return rx.toast.success("Request approved")

    @rx.event
    async def reject_request(self, req_id: str):
        user = await self.get_state(AuthState)
        if user.user_role not in ["Admin", "Manager"]:
            return rx.toast.error("Unauthorized")
        comment = self.manager_comment_input.get(req_id, "")
        for req in self.requests:
            if req.id == req_id:
                req.status = "Rejected"
                req.reviewed_by = user.user.username
                req.reviewed_date = datetime.datetime.now().strftime("%Y-%m-%d")
                req.manager_comment = comment
                msg = f"❌ Leave Request Rejected\nEmployee: {req.employee_username}\nType: {req.leave_type}\nReviewed by: {user.user.username}"
                if await TelegramService.send_message(msg):
                    from app.states.notification_state import NotificationState

                    notif_state = await self.get_state(NotificationState)
                    notif_state.log_telegram_message(msg)
                return rx.toast.success("Request rejected")