import reflex as rx
import uuid
import datetime
from app.models import Notification
from app.states.auth_state import AuthState

MOCK_NOTIFICATIONS: list[Notification] = [
    Notification(
        id="1",
        user_username="admin",
        title="Welcome",
        message="Welcome to the Approval System",
        type="Info",
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
]


class NotificationState(rx.State):
    notifications: list[Notification] = MOCK_NOTIFICATIONS
    telegram_logs: list[str] = []

    @rx.event
    def log_telegram_message(self, message: str):
        """Log a sent telegram message for audit purposes."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.telegram_logs.insert(0, f"[{timestamp}] {message}")

    @rx.var
    def my_notifications(self) -> list[Notification]:
        if not self.user_username:
            return []
        return sorted(
            [n for n in self.notifications if n.user_username == self.user_username],
            key=lambda x: x.created_at,
            reverse=True,
        )

    @rx.var
    def unread_count(self) -> int:
        return len([n for n in self.my_notifications if not n.is_read])

    @rx.var
    def user_username(self) -> str:
        return self.router.page.params.get("username", "") or ""

    @rx.event
    async def add_notification(
        self, username: str, title: str, message: str, type: str = "Info"
    ):
        new_notif = Notification(
            id=str(uuid.uuid4()),
            user_username=username,
            title=title,
            message=message,
            type=type,
            created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
        self.notifications.insert(0, new_notif)

    @rx.event
    async def mark_as_read(self, notif_id: str):
        for n in self.notifications:
            if n.id == notif_id:
                n.is_read = True
                return

    @rx.event
    async def mark_all_as_read(self):
        user = await self.get_state(AuthState)
        if not user.user:
            return
        for n in self.notifications:
            if n.user_username == user.user.username:
                n.is_read = True

    @rx.event
    async def clear_notifications(self):
        user = await self.get_state(AuthState)
        if not user.user:
            return
        self.notifications = [
            n for n in self.notifications if n.user_username != user.user.username
        ]

    @rx.var
    async def get_current_user_name(self) -> str:
        return ""

    @rx.var
    def current_user_notifications(self) -> list[Notification]:
        return self.notifications

    @rx.event
    async def sync_user(self):
        pass

    @rx.var
    def my_notifications(self) -> list[Notification]:
        return self.notifications

    @rx.var
    async def current_user_unread_count(self) -> int:
        user = await self.get_state(AuthState)
        if not user.user:
            return 0
        return len(
            [
                n
                for n in self.notifications
                if n.user_username == user.user.username and (not n.is_read)
            ]
        )

    @rx.var
    async def current_user_notifications_list(self) -> list[Notification]:
        user = await self.get_state(AuthState)
        if not user.user:
            return []
        return sorted(
            [n for n in self.notifications if n.user_username == user.user.username],
            key=lambda x: x.created_at,
            reverse=True,
        )