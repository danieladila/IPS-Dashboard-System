import reflex as rx
from app.states.auth_state import AuthState
from app.components.layout import dashboard_layout


def stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
            class_name=f"p-3 rounded-full bg-{color}-100 mr-4",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 flex items-center",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                f"Welcome back, {AuthState.user.username}!",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Here's what's happening with your requests today.",
                class_name="text-gray-600 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            stat_card("Pending Requests", "12", "clock", "yellow"),
            stat_card("Approved", "45", "check_check", "green"),
            stat_card("Rejected", "3", "circle_x", "red"),
            rx.cond(
                AuthState.user_role == "Admin",
                stat_card("Active Users", "128", "users", "blue"),
                stat_card("My Documents", "8", "file-text", "blue"),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Recent Activity",
                    class_name="text-lg font-semibold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "No recent activity to show.", class_name="text-gray-500 italic"
                    ),
                    class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 min-h-[200px] flex items-center justify-center",
                ),
                class_name="col-span-2",
            ),
            class_name="grid grid-cols-1 gap-6",
        ),
    )


def dashboard_page() -> rx.Component:
    return dashboard_layout(dashboard_content())