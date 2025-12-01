import reflex as rx
from app.states.auth_state import AuthState
from app.pages.auth import login_page, register_page
from app.pages.dashboard import dashboard_page
from app.pages.profile import profile_page


def index() -> rx.Component:
    return rx.el.div(
        "Loading...",
        class_name="flex items-center justify-center min-h-screen text-gray-500",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/styles.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/login", on_load=AuthState.redirect_if_authenticated)
app.add_page(
    register_page, route="/register", on_load=AuthState.redirect_if_authenticated
)
app.add_page(dashboard_page, route="/dashboard", on_load=AuthState.check_login)
app.add_page(profile_page, route="/profile", on_load=AuthState.check_login)
from app.pages.documents import documents_page
from app.pages.leave import leave_page
from app.pages.requests import requests_page
from app.pages.notifications import notifications_page
from app.pages.workflows import workflows_page
from app.pages.users import users_page

app.add_page(documents_page, route="/documents", on_load=AuthState.check_login)
app.add_page(leave_page, route="/leave", on_load=AuthState.check_login)
app.add_page(requests_page, route="/requests", on_load=AuthState.check_login)
app.add_page(notifications_page, route="/notifications", on_load=AuthState.check_login)
app.add_page(workflows_page, route="/workflows", on_load=AuthState.check_login)
app.add_page(users_page, route="/users", on_load=AuthState.check_login)
app.add_page(index, route="/", on_load=AuthState.check_login)