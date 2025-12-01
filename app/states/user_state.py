import reflex as rx
from app.states.auth_state import AuthState, MOCK_USERS
from app.models import User


class UserState(rx.State):
    @rx.var
    def users(self) -> list[User]:
        return MOCK_USERS

    @rx.event
    async def update_role(self, email: str, new_role: str):
        auth_state = await self.get_state(AuthState)
        if auth_state.user_role != "Admin":
            return rx.toast.error("Unauthorized")
        for u in MOCK_USERS:
            if u.email == email:
                u.role = new_role
                return rx.toast.success(f"Updated role for {u.username} to {new_role}")
        return rx.toast.error("User not found")

    @rx.event
    async def delete_user(self, email: str):
        auth_state = await self.get_state(AuthState)
        if auth_state.user_role != "Admin":
            return rx.toast.error("Unauthorized")
        if auth_state.user.email == email:
            return rx.toast.error("Cannot delete your own account")
        for i, u in enumerate(MOCK_USERS):
            if u.email == email:
                MOCK_USERS.pop(i)
                return rx.toast.success("User deleted")
        return rx.toast.error("User not found")