import reflex as rx
from app.states.auth_state import AuthState
from app.states.notification_state import NotificationState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-6 w-6 text-gray-600"),
                class_name="md:hidden p-2 rounded-md hover:bg-gray-100 mr-4",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon(
                            "bell",
                            class_name="h-6 w-6 text-gray-500 hover:text-gray-700",
                        ),
                        rx.cond(
                            NotificationState.current_user_unread_count > 0,
                            rx.el.span(
                                NotificationState.current_user_unread_count,
                                class_name="absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full",
                            ),
                        ),
                        class_name="relative p-2 mr-4",
                    ),
                    href="/notifications",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            AuthState.user.username,
                            class_name="text-sm font-medium text-gray-700",
                        ),
                        rx.el.p(
                            AuthState.user.role, class_name="text-xs text-gray-500"
                        ),
                        class_name="text-right mr-3 hidden sm:block",
                    ),
                    rx.el.div(
                        rx.icon("user", class_name="h-5 w-5 text-gray-600"),
                        class_name="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center border border-gray-200",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="h-5 w-5 text-gray-500"),
                    on_click=AuthState.logout,
                    class_name="ml-4 p-2 rounded-full hover:bg-gray-100 transition-colors",
                    title="Logout",
                ),
                class_name="flex items-center ml-auto",
            ),
            class_name="flex items-center h-16 px-6 bg-white border-b border-gray-200 w-full",
        ),
        class_name="sticky top-0 z-10 w-full",
    )