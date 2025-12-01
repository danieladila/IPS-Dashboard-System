import reflex as rx
from app.components.layout import dashboard_layout
from app.states.user_state import UserState
from app.models import User


def user_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            user.username[0].upper(),
                            class_name="text-sm font-medium text-white",
                        ),
                        class_name="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center",
                    ),
                    class_name="flex-shrink-0 h-10 w-10 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.div(
                        user.username, class_name="text-sm font-medium text-gray-900"
                    ),
                    rx.el.div(user.email, class_name="text-sm text-gray-500"),
                    class_name="ml-4",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(user.role, class_name="text-sm text-gray-900"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                "Active",
                class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            user.created_at,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.select(
                    rx.el.option("Employee", value="Employee"),
                    rx.el.option("Manager", value="Manager"),
                    rx.el.option("Admin", value="Admin"),
                    value=user.role,
                    on_change=lambda val: UserState.update_role(user.email, val),
                    class_name="block w-full pl-3 pr-10 py-1 text-xs border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 rounded-md",
                ),
                rx.el.button(
                    rx.icon(
                        "trash-2", class_name="h-4 w-4 text-red-500 hover:text-red-700"
                    ),
                    on_click=lambda: UserState.delete_user(user.email),
                    class_name="ml-4",
                    title="Delete User",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def users_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "User Management", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Manage system users and roles.",
                    class_name="mt-1 text-sm text-gray-500",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "User",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Role",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Created At",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(UserState.users, user_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
            ),
        )
    )