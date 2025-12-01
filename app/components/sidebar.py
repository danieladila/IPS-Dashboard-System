import reflex as rx
from app.states.auth_state import AuthState


def sidebar_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 mr-3"),
            rx.el.span(text, class_name="font-medium"),
            class_name="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors",
        ),
        href=url,
        class_name="block mb-1",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Industrial Project Service",
                    class_name="text-lg font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-600 tracking-tight leading-tight",
                ),
                class_name="flex items-center h-16 px-6 border-b border-gray-200 bg-slate-50/50",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.el.p(
                        "MENU",
                        class_name="px-4 text-xs font-semibold text-gray-400 tracking-wider mb-2 mt-6",
                    ),
                    sidebar_item("Dashboard", "layout-dashboard", "/dashboard"),
                    sidebar_item("Documents", "file-text", "/documents"),
                    sidebar_item("Leave Requests", "calendar-off", "/leave"),
                    sidebar_item("General Requests", "clipboard-list", "/requests"),
                    sidebar_item("Notifications", "bell", "/notifications"),
                ),
                rx.cond(
                    AuthState.user_role == "Admin",
                    rx.el.div(
                        rx.el.p(
                            "ADMINISTRATION",
                            class_name="px-4 text-xs font-semibold text-gray-400 tracking-wider mb-2 mt-6",
                        ),
                        sidebar_item("Workflows", "git-merge", "/workflows"),
                        sidebar_item("Users", "users", "/users"),
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "SETTINGS",
                        class_name="px-4 text-xs font-semibold text-gray-400 tracking-wider mb-2 mt-6",
                    ),
                    sidebar_item("Profile", "user", "/profile"),
                ),
                class_name="flex-1 overflow-y-auto py-4 px-3",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex w-64 flex-col bg-white border-r border-gray-200 h-screen sticky top-0",
    )