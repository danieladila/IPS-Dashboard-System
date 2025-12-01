import reflex as rx
from typing import Optional
from app.models import User
import hashlib
import datetime

MOCK_USERS: list[User] = []


class AuthState(rx.State):
    user: Optional[User] = None
    error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.user is not None

    @rx.var
    def user_role(self) -> str:
        return self.user.role if self.user else ""

    def _hash_password(self, password: str) -> str:
        salt = b"reflex_approval_system_salt"
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()

    @rx.event
    def login(self, form_data: dict):
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Please fill in all fields"
            return
        found_user = next((u for u in MOCK_USERS if u.email == email), None)
        if found_user and found_user.password_hash == self._hash_password(password):
            self.user = found_user
            self.error_message = ""
            return rx.redirect("/dashboard")
        else:
            self.error_message = "Invalid email or password"

    @rx.event
    def register(self, form_data: dict):
        username = form_data.get("username")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        role = form_data.get("role", "Employee")
        if not username or not email or (not password):
            self.error_message = "Please fill in all fields"
            return
        if password != confirm_password:
            self.error_message = "Passwords do not match"
            return
        if any((u.email == email for u in MOCK_USERS)):
            self.error_message = "Email already registered"
            return
        new_user = User(
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            role=role,
            created_at=datetime.datetime.utcnow().isoformat(),
        )
        MOCK_USERS.append(new_user)
        self.user = new_user
        self.error_message = ""
        return rx.redirect("/dashboard")

    @rx.event
    def logout(self):
        self.user = None
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def redirect_if_authenticated(self):
        if self.is_authenticated:
            return rx.redirect("/dashboard")