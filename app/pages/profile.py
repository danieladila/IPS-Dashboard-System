import reflex as rx
from app.states.auth_state import AuthState
from app.components.layout import dashboard_layout


def profile_field(label: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.el.dt(label, class_name="text-sm font-medium text-gray-500"),
        rx.el.dd(value, class_name="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2"),
        class_name="py-4 sm:grid sm:py-5 sm:grid-cols-3 sm:gap-4",
    )


def profile_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("User Profile", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Manage your account details and settings.",
                class_name="mt-1 text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Personal Information",
                    class_name="text-lg leading-6 font-medium text-gray-900",
                ),
                rx.el.p(
                    "Basic details about your account.",
                    class_name="mt-1 max-w-2xl text-sm text-gray-500",
                ),
                class_name="px-4 py-5 sm:px-6",
            ),
            rx.el.div(
                rx.el.dl(
                    profile_field("Username", AuthState.user.username),
                    profile_field("Email address", AuthState.user.email),
                    profile_field("Role", AuthState.user.role),
                    profile_field(
                        "Account Created", AuthState.user.created_at.to_string()
                    ),
                ),
                class_name="border-t border-gray-200 px-4 py-5 sm:p-0",
            ),
            class_name="bg-white shadow overflow-hidden sm:rounded-lg",
        ),
    )


def profile_page() -> rx.Component:
    return dashboard_layout(profile_content())